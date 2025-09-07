from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import os
import json
from utils.llms import query_groq_llm, query_gemini_llm, query_ollama_llm
from utils.prompts import (
    zero_shot_prompt, one_shot_prompt, few_shot_prompt,
    chain_of_thought_prompt, react_prompt, self_ask_prompt,
    tree_of_thought_prompt, instruction_constraints_prompt,
    persona_based_prompt_template
)
from utils.comparison import run_comparative_evaluation
from utils.report_generator import extract_log_metrics, generate_report
from pathlib import Path
import time
from datetime import datetime

app = Flask(__name__)

# Store session data (in production, use Redis or database)
session_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/prompt-templates')
def get_prompt_templates():
    """Get available prompt templates"""
    templates = {
        "1": {"name": "Zero Shot", "function": "zero_shot_prompt"},
        "2": {"name": "One Shot", "function": "one_shot_prompt"},
        "3": {"name": "Few Shot", "function": "few_shot_prompt"},
        "4": {"name": "Chain of Thought", "function": "chain_of_thought_prompt"},
        "5": {"name": "ReAct", "function": "react_prompt"},
        "6": {"name": "Self Ask", "function": "self_ask_prompt"},
        "7": {"name": "Tree of Thought", "function": "tree_of_thought_prompt"},
        "8": {"name": "Instruction + Constraints", "function": "instruction_constraints_prompt"},
        "9": {"name": "Persona Based", "function": "persona_based_prompt_template"}
    }
    return jsonify(templates)

@app.route('/api/ollama-models')
def get_ollama_models():
    """Get locally installed Ollama models"""
    try:
        # Try different commands based on the system
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            # On Windows, try both with and without .exe extension
            commands_to_try = [
                ["ollama.exe", "list"],
                ["ollama", "list"]
            ]
        else:
            commands_to_try = [["ollama", "list"]]
        
        result = None
        last_error = None
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    check=True,
                    timeout=30  # Add timeout
                )
                break  # Success, exit the loop
            except (subprocess.CalledProcessError, FileNotFoundError) as e:
                last_error = e
                continue
        
        if result is None:
            return jsonify({
                "success": False, 
                "error": f"Ollama not found or not running. Make sure Ollama is installed and running. Last error: {str(last_error)}"
            })
        
        # Parse the output to extract model names
        lines = result.stdout.strip().split('\n')
        models = []
        
        for line in lines[1:]:  # Skip header line
            if line.strip():
                parts = line.split()
                if parts:
                    model_name = parts[0]
                    models.append(model_name)
        
        if not models:
            return jsonify({
                "success": True, 
                "models": result.stdout,
                "parsed_models": [],
                "message": "No models found. Install models with: ollama pull <model-name>"
            })
        
        return jsonify({
            "success": True, 
            "models": result.stdout,
            "parsed_models": models,
            "count": len(models)
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Error running ollama command: {str(e)}"
        })

@app.route('/api/ollama-status')
def check_ollama_status():
    """Check if Ollama service is running"""
    try:
        import platform
        system = platform.system().lower()
        
        if system == "windows":
            commands_to_try = [
                ["ollama.exe", "ps"],
                ["ollama", "ps"]
            ]
        else:
            commands_to_try = [["ollama", "ps"]]
        
        for cmd in commands_to_try:
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    check=True,
                    timeout=10
                )
                return jsonify({
                    "success": True, 
                    "running": True,
                    "message": "Ollama is running",
                    "output": result.stdout
                })
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return jsonify({
            "success": True, 
            "running": False,
            "message": "Ollama is not running or not installed"
        })
        
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e)
        })

@app.route('/api/single-chat', methods=['POST'])
def single_chat():
    """Handle single LLM chat"""
    data = request.json
    provider = data.get('provider')
    model = data.get('model')
    question = data.get('question')
    prompt_template_id = data.get('prompt_template')
    persona_config = data.get('persona_config', {})
    
    try:
        # Get prompt template
        prompt_mapping = {
            "1": zero_shot_prompt,
            "2": one_shot_prompt,
            "3": few_shot_prompt,
            "4": chain_of_thought_prompt,
            "5": react_prompt,
            "6": self_ask_prompt,
            "7": tree_of_thought_prompt,
            "8": instruction_constraints_prompt,
            "9": persona_based_prompt_template
        }
        
        if prompt_template_id == "9":
            role = persona_config.get('role', 'assistant')
            tone = persona_config.get('tone', 'professional')
            style = persona_config.get('style', 'clear and concise')
            prompt = persona_based_prompt_template(role, tone, style)
        else:
            prompt = prompt_mapping[prompt_template_id]()
        
        # Query the LLM
        if provider == "groq":
            response = query_groq_llm(model=model, user_input=question, prompt=prompt)
        elif provider == "gemini":
            response = query_gemini_llm(model=model, user_input=question, prompt=prompt)
        elif provider == "ollama":
            response = query_ollama_llm(model=model, user_input=question, prompt=prompt)
        else:
            return jsonify({"success": False, "error": "Unsupported provider"})
        
        return jsonify({"success": True, "response": response})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/comparative-evaluation', methods=['POST'])
def comparative_evaluation():
    """Handle comparative evaluation"""
    data = request.json
    providers_models = data.get('providers_models', {})
    prompt_templates_config = data.get('prompt_templates', {})
    user_input = data.get('user_input')
    
    try:
        # Build prompt templates
        prompt_templates = {}
        prompt_mapping = {
            "1": zero_shot_prompt,
            "2": one_shot_prompt,
            "3": few_shot_prompt,
            "4": chain_of_thought_prompt,
            "5": react_prompt,
            "6": self_ask_prompt,
            "7": tree_of_thought_prompt,
            "8": instruction_constraints_prompt,
            "9": persona_based_prompt_template
        }
        
        for template_id, config in prompt_templates_config.items():
            if template_id == "9":
                role = config.get('role', 'assistant')
                tone = config.get('tone', 'professional')
                style = config.get('style', 'clear and concise')
                prompt_templates[f"persona_{role}_{tone}_{style}"] = persona_based_prompt_template(role, tone, style)
            else:
                fn = prompt_mapping[template_id]
                prompt_name = fn.__name__.replace('_prompt', '').replace('_', ' ').title()
                prompt_templates[prompt_name] = fn()
        
        # Run comparative evaluation and collect detailed results
        detailed_results = []
        total_tests = 0
        total_time = 0
        successful_tests = 0
        
        for provider, models in providers_models.items():
            for model in models:
                for prompt_name, prompt in prompt_templates.items():
                    total_tests += 1
                    start_time = time.time()
                    
                    try:
                        # Query the specific LLM
                        if provider == "groq":
                            response = query_groq_llm(model=model, user_input=user_input, prompt=prompt)
                        elif provider == "gemini":
                            response = query_gemini_llm(model=model, user_input=user_input, prompt=prompt)
                        elif provider == "ollama":
                            response = query_ollama_llm(model=model, user_input=user_input, prompt=prompt)
                        else:
                            response = f"Unsupported provider: {provider}"
                            
                        response_time = round(time.time() - start_time, 2)
                        total_time += response_time
                        successful_tests += 1
                        
                        detailed_results.append({
                            "provider": provider,
                            "model": model,
                            "prompt_strategy": prompt_name,
                            "question": user_input,
                            "response": response,
                            "response_time": response_time,
                            "success": True
                        })
                        
                    except Exception as e:
                        response_time = round(time.time() - start_time, 2)
                        detailed_results.append({
                            "provider": provider,
                            "model": model,
                            "prompt_strategy": prompt_name,
                            "question": user_input,
                            "error": str(e),
                            "response_time": response_time,
                            "success": False
                        })
        
        # Calculate summary statistics
        avg_response_time = round(total_time / total_tests, 2) if total_tests > 0 else 0
        
        # Find best performer (fastest successful response)
        successful_results = [r for r in detailed_results if r['success']]
        best_performer = "None"
        if successful_results:
            fastest = min(successful_results, key=lambda x: x['response_time'])
            best_performer = f"{fastest['provider']}-{fastest['model']}"
        
        # Store results in session for later use
        session_data['last_comparison'] = {
            'detailed_results': detailed_results,
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'avg_response_time': avg_response_time,
                'best_performer': best_performer
            }
        }
        
        return jsonify({
            "success": True,
            "message": "Comparative evaluation completed",
            "detailed_results": detailed_results,
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "avg_response_time": avg_response_time,
                "best_performer": best_performer
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/generate-report', methods=['POST'])
def generate_report_api():
    """Generate performance report"""
    data = request.json
    user_question = data.get('user_question', '')
    
    try:
        # Use session data if available, otherwise extract from log
        if 'last_comparison' in session_data:
            comparison_data = session_data['last_comparison']
            detailed_results = comparison_data.get('detailed_results', [])
            summary = comparison_data.get('summary', {})
        else:
            # Fallback to log extraction
            summary = extract_log_metrics()
            detailed_results = []
        
        # Create reports directory if it doesn't exist - with absolute path
        reports_dir = os.path.join(os.getcwd(), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate report with proper path handling
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_filename = f'llm_report_{timestamp}.txt'
        report_path = os.path.join(reports_dir, report_filename)

        # Generate the report content
        report_content = f"""LLM COMPARISON REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Question: {user_question}

SUMMARY STATISTICS:
- Total Tests: {summary.get('total_tests', 'N/A')}
- Successful Tests: {summary.get('successful_tests', 'N/A')}
- Average Response Time: {summary.get('avg_response_time', 'N/A')}s
- Best Performer: {summary.get('best_performer', 'N/A')}

DETAILED RESULTS:
"""
        
        if detailed_results:
            for i, result in enumerate(detailed_results, 1):
                status = "✓ SUCCESS" if result.get('success') else "✗ FAILED"
                report_content += f"""
{i}. {result.get('provider', 'Unknown').upper()} - {result.get('model', 'Unknown')}
   Strategy: {result.get('prompt_strategy', 'Unknown')}
   Status: {status}
   Response Time: {result.get('response_time', 'N/A')}s
   Response: {result.get('response', result.get('error', 'No response'))[:200]}...

"""
        else:
            report_content += "\nNo detailed results available. Check the comparison log for more information.\n"
        
        # Write report to file with proper encoding
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # Verify file was created
        if not os.path.exists(report_path):
            raise Exception(f"Failed to create report file at {report_path}")
        
        # Return relative path for download
        return jsonify({
            "success": True, 
            "report_path": report_filename,
            "filename": report_filename,
            "full_path": report_path  # For debugging
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/download-report/<path:filename>')
def download_report(filename):
    """Download generated report"""
    try:
        # Use absolute path
        reports_dir = os.path.join(os.getcwd(), 'reports')
        file_path = os.path.join(reports_dir, filename)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_file(
                file_path, 
                as_attachment=True, 
                download_name=filename,
                mimetype='text/plain'
            )
        else:
            return jsonify({
                "success": False, 
                "error": f"Report file not found: {file_path}",
                "checked_path": file_path,
                "exists": os.path.exists(file_path)
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/get-log')
def get_log():
    """Get comparison log content"""
    try:
        if os.path.exists('llm_comparison.log'):
            with open('llm_comparison.log', 'r') as f:
                content = f.read()
            return jsonify({"success": True, "log_content": content})
        else:
            return jsonify({"success": False, "error": "Log file not found"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)