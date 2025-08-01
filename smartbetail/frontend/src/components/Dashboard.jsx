import { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { 
  UserGroupIcon, 
  ExclamationTriangleIcon, 
  ClockIcon, 
  CalendarDaysIcon,
  HeartIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';
import { smartBetailAPI, useAPI } from '../services/api';

const COLORS = ['#3b82f6', '#ef4444', '#f59e0b', '#10b981', '#8b5cf6', '#f97316'];

function StatCard({ title, value, icon: Icon, trend, color = 'blue' }) {
  const colorClasses = {
    blue: 'bg-smart-blue-50 text-smart-blue-600',
    red: 'bg-red-50 text-red-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    green: 'bg-smart-green-50 text-smart-green-600'
  };

  return (
    <div className="card">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="h-6 w-6" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          {trend && (
            <p className="text-xs text-gray-500 mt-1">{trend}</p>
          )}
        </div>
      </div>
    </div>
  );
}

function RecentDiagnostics({ diagnostics }) {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critique': return 'badge-red';
      case 'élevée': return 'badge-yellow';
      case 'modérée': return 'badge-blue';
      default: return 'badge-green';
    }
  };

  return (
    <div className="card">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Diagnostics Récents</h3>
      <div className="space-y-3">
        {diagnostics.map((diagnostic) => (
          <div key={diagnostic.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <p className="font-medium text-gray-900">{diagnostic.animal.nom}</p>
              <p className="text-sm text-gray-600">{diagnostic.maladie_predite.nom}</p>
              <p className="text-xs text-gray-500">
                Confiance: {(diagnostic.probabilite * 100).toFixed(1)}%
              </p>
            </div>
            <div className="flex flex-col items-end">
              <span className={`badge ${getSeverityColor(diagnostic.maladie_predite.gravite)}`}>
                {diagnostic.maladie_predite.gravite}
              </span>
              <span className="text-xs text-gray-500 mt-1">
                {new Date(diagnostic.date_diagnostic).toLocaleDateString('fr-FR')}
              </span>
            </div>
          </div>
        ))}
        {diagnostics.length === 0 && (
          <p className="text-center text-gray-500 py-8">Aucun diagnostic récent</p>
        )}
      </div>
    </div>
  );
}

function UpcomingCare({ soins }) {
  const getStatusColor = (status, datePreview) => {
    const today = new Date();
    const careDate = new Date(datePreview);
    
    if (careDate < today) return 'badge-red';
    if (careDate.getTime() - today.getTime() <= 3 * 24 * 60 * 60 * 1000) return 'badge-yellow';
    return 'badge-green';
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
    });
  };

  return (
    <div className="card">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Soins à Venir</h3>
      <div className="space-y-3">
        {soins.map((soin) => (
          <div key={soin.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
            <div className="flex-1">
              <p className="font-medium text-gray-900">{soin.animal.nom}</p>
              <p className="text-sm text-gray-600">{soin.nom_soin}</p>
              <p className="text-xs text-gray-500">{soin.type_soin}</p>
            </div>
            <div className="flex flex-col items-end">
              <span className={`badge ${getStatusColor(soin.statut, soin.date_prevue)}`}>
                {formatDate(soin.date_prevue)}
              </span>
              {soin.est_en_retard && (
                <span className="text-xs text-red-600 font-medium mt-1">En retard</span>
              )}
            </div>
          </div>
        ))}
        {soins.length === 0 && (
          <p className="text-center text-gray-500 py-8">Aucun soin planifié</p>
        )}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const { callAPI, loading, error } = useAPI();
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await callAPI(smartBetailAPI.getDashboardData);
      setDashboardData(data);
    } catch (err) {
      console.error('Erreur lors du chargement du dashboard:', err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-smart-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border-red-200">
        <div className="flex items-center">
          <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mr-2" />
          <p className="text-red-700">Erreur lors du chargement du dashboard: {error}</p>
        </div>
      </div>
    );
  }

  if (!dashboardData) {
    return <div>Chargement...</div>;
  }

  // Préparer les données pour les graphiques
  const diseaseChartData = Object.entries(dashboardData.repartition_maladies || {}).map(([name, value]) => ({
    name,
    value
  }));

  const animalTypeChartData = Object.entries(dashboardData.repartition_types_animaux || {}).map(([name, value]) => ({
    name,
    value
  }));

  return (
    <div className="space-y-6">
      {/* En-tête */}
      <div className="border-b border-gray-200 pb-4">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Vue d'ensemble de votre troupeau</p>
      </div>

      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Animaux"
          value={dashboardData.total_animaux}
          icon={UserGroupIcon}
          color="blue"
        />
        <StatCard
          title="Animaux Malades"
          value={dashboardData.animaux_malades}
          icon={HeartIcon}
          color="red"
          trend="Derniers 30 jours"
        />
        <StatCard
          title="Soins en Retard"
          value={dashboardData.soins_en_retard}
          icon={ExclamationTriangleIcon}
          color="yellow"
        />
        <StatCard
          title="Soins cette Semaine"
          value={dashboardData.soins_cette_semaine}
          icon={CalendarDaysIcon}
          color="green"
        />
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Répartition des maladies */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Répartition des Maladies</h3>
          {diseaseChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={diseaseChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {diseaseChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-gray-500 py-8">Aucune donnée disponible</p>
          )}
        </div>

        {/* Répartition par type d'animal */}
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Types d'Animaux</h3>
          {animalTypeChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={animalTypeChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p className="text-center text-gray-500 py-8">Aucune donnée disponible</p>
          )}
        </div>
      </div>

      {/* Listes de données */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RecentDiagnostics diagnostics={dashboardData.diagnostics_recents || []} />
        <UpcomingCare soins={dashboardData.soins_urgents || []} />
      </div>
    </div>
  );
}