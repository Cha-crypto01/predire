import { useState, useEffect } from 'react';
import { smartBetailAPI, useAPI } from '../services/api';
import { 
  CalendarIcon, 
  PlusIcon, 
  PencilIcon, 
  TrashIcon,
  ExclamationTriangleIcon,
  ClockIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';

function AddCareModal({ isOpen, onClose, onSave, animals }) {
  const { callAPI, loading, error, setError } = useAPI();
  const [formData, setFormData] = useState({
    animal_id: '',
    type_soin: 'vaccination',
    nom_soin: '',
    description: '',
    date_prevue: '',
    veterinaire_responsable_id: null
  });

  useEffect(() => {
    if (isOpen) {
      // Réinitialiser le formulaire quand la modal s'ouvre
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      const tomorrowString = tomorrow.toISOString().slice(0, 16); // Format YYYY-MM-DDTHH:MM
      
      setFormData({
        animal_id: '',
        type_soin: 'vaccination',
        nom_soin: '',
        description: '',
        date_prevue: tomorrowString,
        veterinaire_responsable_id: null
      });
      setError(null);
    }
  }, [isOpen, setError]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (!formData.animal_id || !formData.nom_soin || !formData.date_prevue) {
      setError('Veuillez remplir tous les champs obligatoires');
      return;
    }

    try {
      const submitData = {
        ...formData,
        animal_id: parseInt(formData.animal_id),
        veterinaire_responsable_id: formData.veterinaire_responsable_id ? parseInt(formData.veterinaire_responsable_id) : null
      };

      await callAPI(smartBetailAPI.createSchedule, submitData);
      onSave();
      onClose();
    } catch (err) {
      console.error('Erreur lors de la création du soin:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div className="mt-3">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Planifier un Soin</h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
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
                    {animal.nom} ({animal.numero_identification})
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type de soin *
              </label>
              <select
                name="type_soin"
                value={formData.type_soin}
                onChange={handleInputChange}
                className="form-select"
              >
                <option value="vaccination">Vaccination</option>
                <option value="vermifuge">Vermifuge</option>
                <option value="controle">Contrôle vétérinaire</option>
                <option value="traitement">Traitement</option>
                <option value="autre">Autre</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nom du soin *
              </label>
              <input
                type="text"
                name="nom_soin"
                value={formData.nom_soin}
                onChange={handleInputChange}
                className="form-input"
                placeholder="Ex: Vaccination BVD, Vermifugation..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
                className="form-input"
                placeholder="Description du soin..."
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date prévue *
              </label>
              <input
                type="datetime-local"
                name="date_prevue"
                value={formData.date_prevue}
                onChange={handleInputChange}
                className="form-input"
                required
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <div className="flex space-x-3 pt-4">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex-1"
              >
                {loading ? 'Création...' : 'Créer'}
              </button>
              <button
                type="button"
                onClick={onClose}
                className="btn-secondary"
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

function CareCard({ soin, onEdit, onDelete }) {
  const getStatusColor = (status, datePreview, estEnRetard) => {
    if (estEnRetard) return 'border-red-500 bg-red-50';
    
    const today = new Date();
    const careDate = new Date(datePreview);
    
    if (status === 'termine') return 'border-smart-green-500 bg-smart-green-50';
    if (status === 'en_cours') return 'border-smart-blue-500 bg-smart-blue-50';
    if (careDate.getTime() - today.getTime() <= 3 * 24 * 60 * 60 * 1000) return 'border-yellow-500 bg-yellow-50';
    
    return 'border-gray-200 bg-white';
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'planifie': return 'badge-blue';
      case 'en_cours': return 'badge-yellow';
      case 'termine': return 'badge-green';
      case 'reporte': return 'badge-gray';
      case 'annule': return 'badge-red';
      default: return 'badge-gray';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'vaccination': return '💉';
      case 'vermifuge': return '💊';
      case 'controle': return '🔍';
      case 'traitement': return '🏥';
      default: return '📋';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className={`card border-2 ${getStatusColor(soin.statut, soin.date_prevue, soin.est_en_retard)}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center mb-2">
            <span className="text-lg mr-2">{getTypeIcon(soin.type_soin)}</span>
            <h3 className="text-lg font-semibold text-gray-900">{soin.nom_soin}</h3>
          </div>
          
          <p className="text-sm text-gray-600 mb-2">
            <strong>Animal:</strong> {soin.animal.nom} ({soin.animal.numero_identification})
          </p>
          
          <p className="text-sm text-gray-600 mb-2">
            <strong>Date prévue:</strong> {formatDate(soin.date_prevue)}
          </p>
          
          {soin.description && (
            <p className="text-sm text-gray-600 mb-3">{soin.description}</p>
          )}
          
          <div className="flex items-center space-x-2">
            <span className={`badge ${getStatusBadge(soin.statut)}`}>
              {soin.statut.replace('_', ' ')}
            </span>
            
            {soin.est_en_retard && (
              <span className="badge-red">
                <ExclamationTriangleIcon className="h-3 w-3 mr-1" />
                En retard
              </span>
            )}
            
            {soin.jours_jusqu_echeance !== null && soin.jours_jusqu_echeance >= 0 && (
              <span className="text-xs text-gray-500">
                Dans {soin.jours_jusqu_echeance} jour(s)
              </span>
            )}
          </div>
        </div>
        
        <div className="flex space-x-2 ml-4">
          <button
            onClick={() => onEdit(soin)}
            className="p-2 text-gray-400 hover:text-smart-blue-600"
            title="Modifier"
          >
            <PencilIcon className="h-4 w-4" />
          </button>
          <button
            onClick={() => onDelete(soin)}
            className="p-2 text-gray-400 hover:text-red-600"
            title="Supprimer"
          >
            <TrashIcon className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}

export default function Schedule() {
  const { callAPI, loading, error } = useAPI();
  const [soins, setSoins] = useState([]);
  const [animals, setAnimals] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [filter, setFilter] = useState('all'); // all, overdue, upcoming
  const [selectedType, setSelectedType] = useState('all');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [soinsData, animalsData] = await Promise.all([
        callAPI(smartBetailAPI.getSchedule),
        callAPI(smartBetailAPI.getAnimals)
      ]);
      
      setSoins(soinsData.results || soinsData);
      setAnimals(animalsData.results || animalsData);
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err);
    }
  };

  const handleDeleteSoin = async (soin) => {
    if (window.confirm(`Êtes-vous sûr de vouloir supprimer le soin "${soin.nom_soin}" ?`)) {
      try {
        await callAPI(smartBetailAPI.deleteSchedule, soin.id);
        loadData();
      } catch (err) {
        console.error('Erreur lors de la suppression:', err);
      }
    }
  };

  const handleEditSoin = async (soin) => {
    // Pour simplifier, on permet juste de changer le statut
    const nouveauStatut = prompt(
      'Nouveau statut (planifie, en_cours, termine, reporte, annule):',
      soin.statut
    );
    
    if (nouveauStatut && nouveauStatut !== soin.statut) {
      try {
        await callAPI(smartBetailAPI.updateSchedule, soin.id, {
          ...soin,
          statut: nouveauStatut,
          date_realisation: nouveauStatut === 'termine' ? new Date().toISOString() : null
        });
        loadData();
      } catch (err) {
        console.error('Erreur lors de la modification:', err);
      }
    }
  };

  // Filtrer les soins
  const filteredSoins = soins.filter(soin => {
    // Filtre par statut/urgence
    if (filter === 'overdue' && !soin.est_en_retard) return false;
    if (filter === 'upcoming' && (soin.statut !== 'planifie' || soin.est_en_retard)) return false;
    
    // Filtre par type
    if (selectedType !== 'all' && soin.type_soin !== selectedType) return false;
    
    return true;
  });

  // Statistiques
  const stats = {
    total: soins.length,
    enRetard: soins.filter(s => s.est_en_retard).length,
    planifies: soins.filter(s => s.statut === 'planifie').length,
    termines: soins.filter(s => s.statut === 'termine').length
  };

  if (loading && soins.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-smart-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="border-b border-gray-200 pb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <CalendarIcon className="h-8 w-8 text-smart-blue-600 mr-3" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Planification des Soins</h1>
              <p className="text-gray-600">Gestion des vaccinations et soins préventifs</p>
            </div>
          </div>
          
          <button
            onClick={() => setShowAddModal(true)}
            className="btn-primary"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Nouveau Soin
          </button>
        </div>
      </div>

      {/* Statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card bg-smart-blue-50">
          <div className="flex items-center">
            <CalendarIcon className="h-8 w-8 text-smart-blue-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Total Soins</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
            </div>
          </div>
        </div>

        <div className="card bg-red-50">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">En Retard</p>
              <p className="text-2xl font-bold text-gray-900">{stats.enRetard}</p>
            </div>
          </div>
        </div>

        <div className="card bg-yellow-50">
          <div className="flex items-center">
            <ClockIcon className="h-8 w-8 text-yellow-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Planifiés</p>
              <p className="text-2xl font-bold text-gray-900">{stats.planifies}</p>
            </div>
          </div>
        </div>

        <div className="card bg-smart-green-50">
          <div className="flex items-center">
            <CheckCircleIcon className="h-8 w-8 text-smart-green-600" />
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Terminés</p>
              <p className="text-2xl font-bold text-gray-900">{stats.termines}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Filtres */}
      <div className="card">
        <div className="flex flex-wrap items-center gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Filtrer par statut
            </label>
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="form-select"
            >
              <option value="all">Tous les soins</option>
              <option value="overdue">En retard</option>
              <option value="upcoming">À venir</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Type de soin
            </label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="form-select"
            >
              <option value="all">Tous les types</option>
              <option value="vaccination">Vaccination</option>
              <option value="vermifuge">Vermifuge</option>
              <option value="controle">Contrôle vétérinaire</option>
              <option value="traitement">Traitement</option>
              <option value="autre">Autre</option>
            </select>
          </div>
        </div>
      </div>

      {/* Message d'erreur */}
      {error && (
        <div className="card bg-red-50 border-red-200">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mr-2" />
            <p className="text-red-700">Erreur: {error}</p>
          </div>
        </div>
      )}

      {/* Liste des soins */}
      {filteredSoins.length === 0 ? (
        <div className="card text-center py-12">
          <CalendarIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun soin planifié</h3>
          <p className="text-gray-600 mb-4">
            {filter === 'all' 
              ? "Commencez par planifier des soins pour vos animaux."
              : "Aucun soin ne correspond à vos critères de filtrage."
            }
          </p>
          {filter === 'all' && (
            <button
              onClick={() => setShowAddModal(true)}
              className="btn-primary"
            >
              <PlusIcon className="h-5 w-5 mr-2" />
              Planifier un Soin
            </button>
          )}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredSoins.map((soin) => (
            <CareCard
              key={soin.id}
              soin={soin}
              onEdit={handleEditSoin}
              onDelete={handleDeleteSoin}
            />
          ))}
        </div>
      )}

      {/* Modal d'ajout */}
      <AddCareModal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSave={loadData}
        animals={animals}
      />
    </div>
  );
}