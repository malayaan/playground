from tqdm import tqdm
import optuna

def run_optimization(self):
    study = optuna.create_study(direction="maximize")
    
    # Utiliser tqdm pour suivre la progression des essais
    with tqdm(total=self.n_trials, desc="Optimisation en cours") as pbar:
        def callback(study, trial):
            pbar.update(1)  # Mise à jour de la barre de progression
        
        study.optimize(self.objective, n_trials=self.n_trials, callbacks=[callback])
    
    self.best_parameters_ = study.best_params
    self.best_metric_value = study.best_value
    return study