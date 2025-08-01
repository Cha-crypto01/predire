import { useState, useEffect } from 'react';
import { smartBetailAPI, useAPI } from '../services/api';
import { 
  CpuChipIcon, 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  InformationCircleIcon 
} from '@heroicons/react/24/outline';

export default function Predict() {
  const { callAPI, loading, error, setError } = useAPI();
  const [animals, setAnimals] = useState([]);
  const [formData, setFormData] = useState({
    animal_id: '',
    temperature: '',
    frequence_cardiaque: '',
    frequence_respiratoire: '',
    niveau_activite: 3,
    appetit: 3,
    fievre: false,
    toux: false,
    diarrhee: false,
    ecoulement_nasal: false,
    boiterie: false,
    abattement: false,
    perte_poids: false,
    notes_veterinaire: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    loadAnimals();
  }, []);

  const loadAnimals = async () => {
    try {
      const data = await callAPI(smartBetailAPI.getAnimals);
      setAnimals(data.results || data);
    } catch (err) {
      console.error('Erreur lors du chargement des animaux:', err);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      setFormData(prev => ({ ...prev, [name]: checked }));
    } else if (type === 'number') {
      setFormData(prev => ({ ...prev, [name]: value ? parseFloat(value) : '' }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setPrediction(null);
    setShowResult(false);

    // Validation
    if (!formData.animal_id) {
      setError('Veuillez sélectionner un animal');
      return;
    }

    try {
      // Préparer les données pour l'API
      const predictionData = {
        ...formData,
        animal_id: parseInt(formData.animal_id),
        niveau_activite: parseInt(formData.niveau_activite),
        appetit: parseInt(formData.appetit)
      };

      // Supprimer les champs vides pour les valeurs numériques optionnelles
      if (!predictionData.temperature) delete predictionData.temperature;
      if (!predictionData.frequence_cardiaque) delete predictionData.frequence_cardiaque;
      if (!predictionData.frequence_respiratoire) delete predictionData.frequence_respiratoire;

      const result = await callAPI(smartBetailAPI.predictDisease, predictionData);
      setPrediction(result);
      setShowResult(true);
    } catch (err) {
      console.error('Erreur lors de la prédiction:', err);
    }
  };

  const resetForm = () => {
    setFormData({
      animal_id: '',
      temperature: '',
      frequence_cardiaque: '',
      frequence_respiratoire: '',
      niveau_activite: 3,
      appetit: 3,
      fievre: false,
      toux: false,
      diarrhee: false,
      ecoulement_nasal: false,
      boiterie: false,
      abattement: false,
      perte_poids: false,
      notes_veterinaire: ''
    });
    setPrediction(null);
    setShowResult(false);
    setError(null);
  };

  const getConfidenceColor = (niveau) => {
    switch (niveau) {
      case 'Très élevé': return 'text-smart-green-600';
      case 'Élevé': return 'text-smart-blue-600';
      case 'Modéré': return 'text-yellow-600';
      default: return 'text-red-600';
    }
  };

  const getSeverityBadge = (gravite) => {
    switch (gravite) {
      case 'critique': return 'badge-red';
      case 'élevée': return 'badge-yellow';
      case 'modérée': return 'badge-blue';
      default: return 'badge-green';
    }
  };

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="border-b border-gray-200 pb-4">
        <div className="flex items-center">
          <CpuChipIcon className="h-8 w-8 text-smart-blue-600 mr-3" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Prédiction IA</h1>
            <p className="text-gray-600">Diagnostic intelligent basé sur les symptômes observés</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Formulaire de saisie */}
        <div className="card">
          <h2 className="text-lg font-medium text-gray-900 mb-6">Symptômes Observés</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Sélection de l'animal */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Animal *
              </label>
              <select
                name="animal_id"
                value={formData.animal_id}
                onChange={handleInputChange}
                className="form-select"
                required
              >
                <option value="">Sélectionner un animal</option>
                {animals.map((animal) => (
                  <option key={animal.id} value={animal.id}>
                    {animal.nom} ({animal.numero_identification}) - {animal.type_animal}
                  </option>
                ))}
              </select>
            </div>

            {/* Données vitales */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Données Vitales</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Température (°C)
                  </label>
                  <input
                    type="number"
                    name="temperature"
                    value={formData.temperature}
                    onChange={handleInputChange}
                    step="0.1"
                    min="35"
                    max="45"
                    className="form-input"
                    placeholder="38.5"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fréquence cardiaque (bpm)
                  </label>
                  <input
                    type="number"
                    name="frequence_cardiaque"
                    value={formData.frequence_cardiaque}
                    onChange={handleInputChange}
                    min="40"
                    max="120"
                    className="form-input"
                    placeholder="70"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fréquence respiratoire
                  </label>
                  <input
                    type="number"
                    name="frequence_respiratoire"
                    value={formData.frequence_respiratoire}
                    onChange={handleInputChange}
                    min="10"
                    max="60"
                    className="form-input"
                    placeholder="25"
                  />
                </div>
              </div>
            </div>

            {/* Comportement */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Comportement</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Niveau d'activité
                  </label>
                  <select
                    name="niveau_activite"
                    value={formData.niveau_activite}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option value={1}>1 - Très faible</option>
                    <option value={2}>2 - Faible</option>
                    <option value={3}>3 - Normal</option>
                    <option value={4}>4 - Élevé</option>
                    <option value={5}>5 - Très élevé</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Appétit
                  </label>
                  <select
                    name="appetit"
                    value={formData.appetit}
                    onChange={handleInputChange}
                    className="form-select"
                  >
                    <option value={1}>1 - Aucun appétit</option>
                    <option value={2}>2 - Appétit faible</option>
                    <option value={3}>3 - Appétit normal</option>
                    <option value={4}>4 - Bon appétit</option>
                    <option value={5}>5 - Appétit excessif</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Symptômes observables */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-gray-900">Symptômes Observables</h3>
              
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {[
                  { name: 'fievre', label: 'Fièvre' },
                  { name: 'toux', label: 'Toux' },
                  { name: 'diarrhee', label: 'Diarrhée' },
                  { name: 'ecoulement_nasal', label: 'Écoulement nasal' },
                  { name: 'boiterie', label: 'Boiterie' },
                  { name: 'abattement', label: 'Abattement' },
                  { name: 'perte_poids', label: 'Perte de poids' }
                ].map((symptom) => (
                  <label key={symptom.name} className="flex items-center">
                    <input
                      type="checkbox"
                      name={symptom.name}
                      checked={formData[symptom.name]}
                      onChange={handleInputChange}
                      className="rounded border-gray-300 text-smart-blue-600 focus:ring-smart-blue-500"
                    />
                    <span className="ml-2 text-sm text-gray-700">{symptom.label}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Notes */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Notes vétérinaire
              </label>
              <textarea
                name="notes_veterinaire"
                value={formData.notes_veterinaire}
                onChange={handleInputChange}
                rows={3}
                className="form-input"
                placeholder="Observations supplémentaires..."
              />
            </div>

            {/* Erreur */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <div className="flex">
                  <ExclamationTriangleIcon className="h-5 w-5 text-red-400" />
                  <div className="ml-3">
                    <p className="text-sm text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Boutons */}
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex-1"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Analyse en cours...
                  </div>
                ) : (
                  'Analyser les symptômes'
                )}
              </button>
              
              <button
                type="button"
                onClick={resetForm}
                className="btn-secondary"
              >
                Réinitialiser
              </button>
            </div>
          </form>
        </div>

        {/* Résultats de la prédiction */}
        <div className="space-y-6">
          {showResult && prediction && (
            <div className="card">
              <h2 className="text-lg font-medium text-gray-900 mb-6">Résultats du Diagnostic IA</h2>
              
              {/* Maladie prédite */}
              <div className="bg-smart-blue-50 rounded-lg p-4 mb-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-gray-900">
                      {prediction.maladie_predite.nom}
                    </h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {prediction.maladie_predite.description}
                    </p>
                  </div>
                  <span className={`badge ${getSeverityBadge(prediction.maladie_predite.gravite)}`}>
                    {prediction.maladie_predite.gravite}
                  </span>
                </div>
                
                <div className="mt-4">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-700">Niveau de confiance</span>
                    <span className={`font-semibold ${getConfidenceColor(prediction.niveau_confiance)}`}>
                      {prediction.niveau_confiance} ({(prediction.probabilite * 100).toFixed(1)}%)
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                    <div
                      className="bg-smart-blue-600 h-2 rounded-full"
                      style={{ width: `${prediction.probabilite * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              {/* Traitement recommandé */}
              {prediction.traitement_recommande && (
                <div className="bg-smart-green-50 rounded-lg p-4 mb-6">
                  <h4 className="font-semibold text-gray-900 mb-2">Traitement Recommandé</h4>
                  <div className="space-y-2 text-sm">
                    <p><strong>Traitement:</strong> {prediction.traitement_recommande.nom}</p>
                    <p><strong>Dosage:</strong> {prediction.traitement_recommande.dosage}</p>
                    <p><strong>Durée:</strong> {prediction.traitement_recommande.duree_jours} jours</p>
                    {prediction.traitement_recommande.contre_indications && (
                      <p><strong>Contre-indications:</strong> {prediction.traitement_recommande.contre_indications}</p>
                    )}
                  </div>
                </div>
              )}

              {/* Recommandations */}
              <div className="bg-yellow-50 rounded-lg p-4">
                <h4 className="font-semibold text-gray-900 mb-3">Recommandations</h4>
                <ul className="space-y-2">
                  {prediction.recommandations.map((recommandation, index) => (
                    <li key={index} className="flex items-start">
                      <InformationCircleIcon className="h-4 w-4 text-yellow-600 mr-2 mt-0.5 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{recommandation}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Avertissement */}
              <div className="bg-orange-50 border border-orange-200 rounded-md p-4">
                <div className="flex">
                  <ExclamationTriangleIcon className="h-5 w-5 text-orange-400" />
                  <div className="ml-3">
                    <p className="text-sm text-orange-700">
                      <strong>Important:</strong> Ce diagnostic automatique est une aide à la décision. 
                      Il ne remplace pas l'expertise d'un vétérinaire qualifié. 
                      Consultez toujours un professionnel pour confirmation et traitement.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Aide à l'utilisation */}
          {!showResult && (
            <div className="card bg-gray-50">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Guide d'utilisation</h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start">
                  <CheckCircleIcon className="h-4 w-4 text-smart-green-600 mr-2 mt-0.5" />
                  <span>Sélectionnez l'animal à examiner</span>
                </div>
                <div className="flex items-start">
                  <CheckCircleIcon className="h-4 w-4 text-smart-green-600 mr-2 mt-0.5" />
                  <span>Renseignez les données vitales si disponibles</span>
                </div>
                <div className="flex items-start">
                  <CheckCircleIcon className="h-4 w-4 text-smart-green-600 mr-2 mt-0.5" />
                  <span>Évaluez le comportement (activité, appétit)</span>
                </div>
                <div className="flex items-start">
                  <CheckCircleIcon className="h-4 w-4 text-smart-green-600 mr-2 mt-0.5" />
                  <span>Cochez les symptômes observés</span>
                </div>
                <div className="flex items-start">
                  <CheckCircleIcon className="h-4 w-4 text-smart-green-600 mr-2 mt-0.5" />
                  <span>Lancez l'analyse pour obtenir un diagnostic IA</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}