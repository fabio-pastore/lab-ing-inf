from revanalysis.AnalysisEngine import AnalysisEngine

if __name__ == "__main__":

    print("[Main] SENTIMENT-ANALYSIS V-1.0 BY")
    print(r"""============================================================
     .-.               ___                    
    /    \            (   )      .-.           
    | .`. ;    .---.   | |.-.   ( __)   .--.   
    | |(___)  / .-, \  | /   \  (''")  /    \  
    | |_     (__) ; |  |  .-. |  | |  |  .-. ; 
    (   __)     .'`  |  | |  | |  | |  | |  | | 
    | |       / .'| |  | |  | |  | |  | |  | | 
    | |      | /  | |  | |  | |  | |  | |  | | 
    | |      ; |  ; |  | '  | |  | |  | '  | | 
    | |      ' `-'  |  ' `-' ;   | |  '  `-' / 
    (___)     `.__.'_.   `.__.   (___)  `.__.'    
============================================================""")

    ae: AnalysisEngine = AnalysisEngine()
    ae.start_analysis()

    print("Process exited with status code (0)")
