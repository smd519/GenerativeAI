from flask import Flask, render_template, request
import os
from DataAnalysis import DataAnalysis
from BIAgent import BIAgent
from BAAgent import BAAgent
from SupervisorAgent import SupervisorAgent

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    bi_results = None  # Initialize bi_results to None
    if request.method == 'POST':
        api_key = request.form['api_key']
        file_path = request.form['file_path']
        analysis_type = request.form['analysis_type']
        prompt_type = request.form['prompt_type']
        
        # Trigger the main function
        bi_results = main(api_key, file_path, analysis_type, prompt_type)
    
    return render_template('index.html', bi_results=bi_results)

def main(api_key, file_path, analysis_type, prompt_type):
    data_analysis = DataAnalysis(file_path, analysis_type)
    
    # Generate a plot
    plot_file_path = 'plots/plot.png'  # Path where the plot will be saved
    # # Example plotting (replace with your actual plotting logic)
    # plt.plot(data_analysis.load_data()['column_name'])  # Replace with your data column
    # plt.title('Data Analysis Plot')
    # plt.savefig(plot_file_path)
    # plt.close()

    # Generate results
    sale_anomalies = data_analysis.get_performance_matrix()
    sale_anomalies = sale_anomalies if not sale_anomalies.empty else "There is no anomaly"

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

    bi_agent = BIAgent(api_key, prompt_type)
    bi_results = bi_agent.generate_message(input_data)
    
    return bi_results, plot_file_path  # Return both results and plot URL

if __name__ == '__main__':
    app.run(debug=True)