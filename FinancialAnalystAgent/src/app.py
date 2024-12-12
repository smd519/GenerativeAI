from flask import Flask, render_template,  request, jsonify, session
import os
from models.DataAnalysis import DataAnalysis
from models.BIAgent import BIAgent
from models.BAAgent import BAAgent
from models.SupervisorAgent import SupervisorAgent
from openai import OpenAI

app = Flask(__name__)
# We need this to share some variable btw APIs
app.secret_key = os.urandom(24)

@app.route('/home', methods=['GET', 'POST'])
def home():
    results = None  # Initialize bi_results to None
    plot_file_path = None
    table_data = None
    if request.method == 'POST':
        api_key = request.form['api_key']
        file_path = request.form['file_path']
        analysis_type = request.form['analysis_type']
        prompt_type = request.form['prompt_type']
        
        # Trigger the main function
        results, plot_file_path, table_data = main(api_key, file_path, analysis_type, prompt_type)

    return render_template('home.html', results = results, plot_url = plot_file_path, table_data = table_data)


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None  # Initialize bi_results to None
    plot_file_path = None
    table_data = None
    if request.method == 'POST':
        api_key = request.form['api_key']
        file_path = request.form['file_path']
        analysis_type = request.form['analysis_type']
        prompt_type = request.form['prompt_type']
        
        # Trigger the main function
        results, plot_file_path, table_data = main(api_key, file_path, analysis_type, prompt_type)

    return render_template('index.html', results = results, plot_url = plot_file_path, table_data = table_data)

def main(api_key, file_path, analysis_type, prompt_type):
    data_analysis = DataAnalysis(file_path, analysis_type)
    
    # Generate a plot
    plot_file_path = 'static/plot.jpg'  # Path where the plot will be saved
    # plt.plot(data_analysis.load_data()['YoY'])
    # plt.title('Data Analysis Plot')
    # plt.savefig(plot_file_path)
    # plt.close()

    # Generate results
    sale_anomalies = data_analysis.get_performance_matrix()
    sale_anomalies = sale_anomalies if not sale_anomalies.empty else "There is no anomaly"
    print(sale_anomalies)
    table_data = format_results(sale_anomalies)
    print(table_data)

    demand_anomalies = data_analysis.get_demand_matrix()
    demand_anomalies = demand_anomalies if not demand_anomalies.empty else "There is no anomaly"

    supply_anomalies = data_analysis.get_supply_matrix()
    supply_anomalies = supply_anomalies if not supply_anomalies.empty else "There is no anomaly"

    outlook_anomalies = data_analysis.get_outlook_matrix()
    outlook_anomalies = outlook_anomalies if not outlook_anomalies.empty else "There is no anomaly"

    input_data = {
        "sale_anomalies": sale_anomalies,
        "demand_anomalies": demand_anomalies,
        "supply_anomalies": supply_anomalies,
        "outlook_anomalies": outlook_anomalies
    }

    single_agent_sys = [
        "single_agent_zero_shot",
        "single_agent_one_shot",
        "single_agent_few_shot",
        "single_agent_cot"]
    two_agent_sys = []
    four_agent_sys = ["multi_agent_cot"]
    if prompt_type in single_agent_sys:
        print("single_agent_sys")
        bi_agent = BIAgent(api_key, prompt_type)
        bi_results = bi_agent.process(input_data)
        # bi_results = """
        # Test TEST TESTTest TEST TEST
        # """
        print(bi_results)
        final_results = bi_results
    elif prompt_type in two_agent_sys:
        print("two_agent_sys")
        bi_agent = BIAgent(api_key, prompt_type)
        bi_results = bi_agent.generate_message(input_data)

        ba_agent = BAAgent(api_key, prompt_type)
        ba_results = ba_agent.generate_message(bi_results)
        final_results = ba_results
    elif prompt_type in four_agent_sys:
        print("four_agent_sys")
        bi_agent = BIAgent(api_key, prompt_type)
        bi_results = bi_agent.generate_message(input_data)

        ba_agent = BAAgent(api_key, prompt_type)
        ba_results = ba_agent.generate_message(bi_results)

        supervisor_agent = SupervisorAgent(api_key, prompt_type)
        supervisor_results = supervisor_agent.generate_message(bi_results)
        final_results = supervisor_results

    # Store the final_results and input_data for follow up questions
    # not the best approach- it makes APIs dependent but that's what we need
    #session['input_data'] = input_data
    session['final_results'] = final_results
    session['api_key'] = api_key
    
    return final_results, plot_file_path, table_data  # Return both results and plot URL

# cant think of a better name?
@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Access 'final_results' and 'input_data' from session
    final_results = session.get('final_results')
    api_key = session.get('api_key')
    # input_data = session.get('input_data')
    # print(input_data)

    # If no data is available in session, return an error
    if not final_results:
        return jsonify({'error': 'No previous analysis data available'}), 400

    # Initialize conversation history if not already in session
    if 'conversation_history' not in session:
        session['conversation_history'] = []
        print("conversation_history created")

    # Get the last_response from the session
    last_response = final_results
    if session['conversation_history']:
        for message in reversed(session['conversation_history']):
            last_response = message
            print("last_response retrieved")
            print(last_response)
            break

    # Prepare the conversation for the OpenAI API
    messages = []
    messages.append({
        'role': 'system',
        'content': 'You are a financial data analyst. Focus on presenting precise key quantitative insights based on response listed in assistant propmpt.'
    })
    if last_response:
        messages.append({
            'role': 'assistant',
            'content': last_response
        })
    messages.append({
        'role': 'user',
        'content': user_message
    })

    # Call OpenAI API for a response
    try:
        openai_client = OpenAI(api_key = api_key)
        response = openai_client.chat.completions.create(
                    model = "gpt-4o-mini",
                    messages = messages
                    )
        agent_message = response.choices[0].message.content
        session['conversation_history'].append(agent_message)
        return jsonify({'response': agent_message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def format_results(results):
    """
    convert the sale_anomalies from DataAnalysis into a list of dictionaries that match the expected format for the table.
    """

    results = results[ results['accounting_period_type'] == 'L7D']
    formatted_results = results.to_dict(orient='records')

    return formatted_results


if __name__ == '__main__':
    app.run(debug=True)