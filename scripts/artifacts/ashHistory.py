import os

from scripts.artifact_report import ArtifactHtmlReport
from scripts.lleapfuncs import logfunc, tsv, get_next_unused_name, get_user_name_from_home


def get_python_history(files_found, report_folder, seeker, wrap_text):

    for file_found in files_found:
        file_found = str(file_found)
        data_list = []
        data_headers = []
        user_name = get_user_name_from_home(file_found)
        with open(file_found, 'r') as f:
            lines = f.readlines()
            for line in lines:
                temp_data_list = []
                temp_data_list = ((user_name, line, file_found))
                data_list.append(temp_data_list)

        usageentries = len(data_list)
        if usageentries > 0:
            report = ArtifactHtmlReport(f'Python History of {user_name}')
            #check for existing and get next name for report file, so report from another file does not get overwritten
            report_path = os.path.join(report_folder, f'python_history_{user_name}.temphtml')
            report_path = get_next_unused_name(report_path)[:-9] # remove .temphtml
            report.start_artifact_report(report_folder, os.path.basename(report_path))
            report.add_script()
            data_headers = ['user_name', 'command', 'sourcefile']

            report.write_artifact_data_table(data_headers, data_list, file_found)
            report.end_artifact_report()
            
            tsvname = f'python_history_{user_name}'
            tsv(report_folder, data_headers, data_list, tsvname)
            
        else:
            logfunc(f'No python history data for {user_name}available')

__artifacts__ = {
        "python_history": (
                "Python History",
                ('**/home/*/.python_history'),
                get_bash_history)
}
