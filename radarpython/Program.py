from NsrRadarSdk import *

class NsrRadarDemo: #this class replaces the original namespace 'NsrRadarDemo'
    class Program:
        #/ <summary>
        #/ 应用程序的主入口点。
        #/ </summary>
# C# TO PYTHON CONVERTER TASK: C# attributes do not have Python equivalents:
# ORIGINAL LINE: [STAThread] static void Main()
        @staticmethod
        def Main():
            Application.EnableVisualStyles()
            Application.SetCompatibleTextRenderingDefault(False)
            Application.Run(FormRadarManage())
