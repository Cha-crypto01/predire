import { useState, useEffect } from 'react';
import { smartBetailAPI, useAPI } from '../services/api';
import { 
  UserGroupIcon, 
  ExclamationTriangleIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline';

function AnimalCard({ animal }) {
  const getTypeIcon = (type) => {
    switch (type) {
      case 'bovin': return '🐄';
      case 'ovin': return '🐑';
      case 'caprin': return '🐐';
      case 'porcin': return '🐷';
      case 'équidé': return '🐴';
      default: return '🐾';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div className="flex items-center">
          <span className="text-2xl mr-3">{getTypeIcon(animal.type_animal)}</span>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{animal.nom}</h3>
            <p className="text-sm text-gray-600">{animal.numero_identification}</p>
          </div>
        </div>
        <span className="badge-blue">{animal.type_animal}</span>
      </div>
      
      <div className="mt-4 space-y-2">
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-600">Race:</span>
            <span className="ml-2 font-medium">{animal.race}</span>
          </div>
          <div>
            <span className="text-gray-600">Sexe:</span>
            <span className="ml-2 font-medium">{animal.sexe === 'M' ? 'Mâle' : 'Femelle'}</span>
          </div>
          <div>
            <span className="text-gray-600">Naissance:</span>
            <span className="ml-2 font-medium">{formatDate(animal.date_naissance)}</span>
          </div>
          <div>
            <span className="text-gray-600">Âge:</span>
            <span className="ml-2 font-medium">{animal.age_months} mois</span>
          </div>
        </div>
        
        {animal.poids && (
          <div className="text-sm">
            <span className="text-gray-600">Poids:</span>
            <span className="ml-2 font-medium">{animal.poids} kg</span>
          </div>
        )}
        
        <div className="text-xs text-gray-500 pt-2 border-t">
          Propriétaire: {animal.proprietaire.first_name} {animal.proprietaire.last_name}
        </div>
      </div>
    </div>
  );
}

export default function Animals() {
  const { callAPI, loading, error } = useAPI();
  const [animals, setAnimals] = useState([]);
  const [filter, setFilter] = useState('all');

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

  // Filtrer les animaux par type
  const filteredAnimals = animals.filter(animal => {
    if (filter === 'all') return true;
    return animal.type_animal === filter;
  });

  // Statistiques
  const stats = {
    total: animals.length,
    bovins: animals.filter(a => a.type_animal === 'bovin').length,
    ovins: animals.filter(a => a.type_animal === 'ovin').length,
    caprins: animals.filter(a => a.type_animal === 'caprin').length,
    porcins: animals.filter(a => a.type_animal === 'porcin').length,
    équidés: animals.filter(a => a.type_animal === 'équidé').length
  };

  if (loading) {
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
        <div className="flex items-center">
          <UserGroupIcon className="h-8 w-8 text-smart-blue-600 mr-3" />
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Gestion des Animaux</h1>
            <p className="text-gray-600">Liste et informations de votre troupeau</p>
          </div>
        </div>
      </div>

      {/* Statistiques */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="card bg-smart-blue-50 text-center">
          <div className="text-2xl mb-1">🐾</div>
          <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
          <div className="text-sm text-gray-600">Total</div>
        </div>
        
        <div className="card bg-green-50 text-center">
          <div className="text-2xl mb-1">🐄</div>
          <div className="text-2xl font-bold text-gray-900">{stats.bovins}</div>
          <div className="text-sm text-gray-600">Bovins</div>
        </div>
        
        <div className="card bg-yellow-50 text-center">
          <div className="text-2xl mb-1">🐑</div>
          <div className="text-2xl font-bold text-gray-900">{stats.ovins}</div>
          <div className="text-sm text-gray-600">Ovins</div>
        </div>
        
        <div className="card bg-purple-50 text-center">
          <div className="text-2xl mb-1">🐐</div>
          <div className="text-2xl font-bold text-gray-900">{stats.caprins}</div>
          <div className="text-sm text-gray-600">Caprins</div>
        </div>
        
        <div className="card bg-pink-50 text-center">
          <div className="text-2xl mb-1">🐷</div>
          <div className="text-2xl font-bold text-gray-900">{stats.porcins}</div>
          <div className="text-sm text-gray-600">Porcins</div>
        </div>
        
        <div className="card bg-orange-50 text-center">
          <div className="text-2xl mb-1">🐴</div>
          <div className="text-2xl font-bold text-gray-900">{stats.équidés}</div>
          <div className="text-sm text-gray-600">Équidés</div>
        </div>
      </div>

      {/* Filtres */}
      <div className="card">
        <div className="flex items-center gap-4">
          <label className="block text-sm font-medium text-gray-700">
            Filtrer par type:
          </label>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="form-select"
          >
            <option value="all">Tous les animaux</option>
            <option value="bovin">Bovins</option>
            <option value="ovin">Ovins</option>
            <option value="caprin">Caprins</option>
            <option value="porcin">Porcins</option>
            <option value="équidé">Équidés</option>
          </select>
          
          <div className="ml-auto text-sm text-gray-600">
            {filteredAnimals.length} animal(s) affiché(s)
          </div>
        </div>
      </div>

      {/* Message d'erreur */}
      {error && (
        <div className="card bg-red-50 border-red-200">
          <div className="flex items-center">
            <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mr-2" />
            <p className="text-red-700">Erreur lors du chargement: {error}</p>
          </div>
        </div>
      )}

      {/* Liste des animaux */}
      {filteredAnimals.length === 0 ? (
        <div className="card text-center py-12">
          <UserGroupIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {filter === 'all' ? 'Aucun animal enregistré' : `Aucun ${filter} trouvé`}
          </h3>
          <p className="text-gray-600">
            {filter === 'all' 
              ? 'Commencez par ajouter des animaux à votre troupeau.'
              : 'Essayez de changer le filtre pour voir d\'autres animaux.'
            }
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAnimals.map((animal) => (
            <AnimalCard key={animal.id} animal={animal} />
          ))}
        </div>
      )}

      {/* Informations */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="flex items-start">
          <InformationCircleIcon className="h-5 w-5 text-blue-500 mr-3 mt-0.5" />
          <div className="text-sm text-blue-700">
            <p className="font-medium mb-1">Information</p>
            <p>
              Cette page affiche tous les animaux de votre troupeau. 
              Pour ajouter de nouveaux animaux ou modifier les informations existantes, 
              utilisez l'interface d'administration Django à l'adresse{' '}
              <a href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer" className="underline">
                /admin/
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}