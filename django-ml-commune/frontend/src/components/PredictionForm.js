import React, { useState } from 'react';
import axios from 'axios';

const PredictionForm = () => {
    const [commune, setCommune] = useState('');
    const [year, setYear] = useState('');
    const [prediction, setPrediction] = useState(null);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setPrediction(null);

        try {
            const response = await axios.post('/api/predict/', { commune, year });
            setPrediction(response.data.prediction);
        } catch (err) {
            setError('Erreur lors de la prédiction. Veuillez vérifier vos données.');
        }
    };

    return (
        <div>
            <h2>Prédiction des recettes et dépenses</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>
                        Commune:
                        <select value={commune} onChange={(e) => setCommune(e.target.value)} required>
                            <option value="">Sélectionnez une commune</option>
                            <option value="Commune1">Commune1</option>
                            <option value="Commune2">Commune2</option>
                            <option value="Commune3">Commune3</option>
                        </select>
                    </label>
                </div>
                <div>
                    <label>
                        Année:
                        <input
                            type="number"
                            value={year}
                            onChange={(e) => setYear(e.target.value)}
                            required
                        />
                    </label>
                </div>
                <button type="submit">Prédire</button>
            </form>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {prediction && <p>Prédiction: {prediction}</p>}
        </div>
    );
};

export default PredictionForm;