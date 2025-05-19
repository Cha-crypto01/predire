import React from 'react';
import PredictionForm from './components/PredictionForm';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Prédiction des Recettes et Dépenses d'une Commune</h1>
            </header>
            <main>
                <PredictionForm />
            </main>
        </div>
    );
}

export default App;