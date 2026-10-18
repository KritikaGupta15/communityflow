import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

// Helper component to handle smooth map panning when a neighborhood is clicked
function MapController({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

export default function App() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Filter states
  const [minTransit, setMinTransit] = useState(0);
  const [minParks, setMinParks] = useState(0);
  const [minLibraries, setMinLibraries] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');

  // Map focus state
  const [mapCenter, setMapCenter] = useState([41.8781, -87.6298]);
  const [mapZoom, setMapZoom] = useState(11);
  const [selectedId, setSelectedId] = useState(null);

  const fetchRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/recommendations`, {
        params: {
          min_transit_score: minTransit,
          min_parks: minParks,
          min_libraries: minLibraries
        }
      });
      setRecommendations(response.data.recommendations || []);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      setRecommendations([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecommendations();
  }, [minTransit, minParks, minLibraries]);

  // Filter recommendations locally by name search query
  const filteredRecommendations = recommendations.filter(n =>
    n.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Handle clicking a card in the sidebar
  const handleSelectNeighborhood = (n) => {
    setSelectedId(n.id);
    if (n.latitude && n.longitude) {
      setMapCenter([n.latitude, n.longitude]);
      setMapZoom(14); // Zoom in closer on selection
    }
  };

  // Export filtered locations to CSV
  const exportToCSV = () => {
    if (filteredRecommendations.length === 0) return;
    
    const headers = ["Name", "Wellness Score", "Transit Score", "Parks Count", "Libraries Count", "Latitude", "Longitude"];
    const rows = filteredRecommendations.map(n => [
      `"${n.name}"`,
      n.wellness_score,
      n.transit_score,
      n.parks_count,
      n.libraries_count,
      n.latitude,
      n.longitude
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows.map(e => e.join(","))].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", "communityflow_chicago_wellness.csv");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', margin: 0, padding: 0, overflow: 'hidden' }}>
      
      {/* SIDEBAR CONTROLS & LIST */}
      <div style={{ width: '420px', backgroundColor: '#f8f9fa', padding: '20px', boxSizing: 'border-box', overflowY: 'auto', borderRight: '1px solid #dee2e6', display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <div>
          <h2 style={{ margin: '0 0 5px 0', color: '#2c3e50' }}>CommunityFlow Chicago</h2>
          <p style={{ margin: 0, color: '#7f8c8d', fontSize: '14px' }}>Wellness Infrastructure Platform for Yoga Instructors</p>
        </div>

        {/* SEARCH & FILTERS PANEL */}
        <div style={{ background: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <h3 style={{ margin: '0', fontSize: '16px', color: '#34495e' }}>Filter & Search</h3>
          
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px', color: '#555' }}>Search Neighborhood</label>
            <input 
              type="text" 
              placeholder="e.g., Lincoln Park, Loop..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ width: '100%', padding: '8px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #ccc', fontSize: '13px' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px', color: '#555' }}>Min Transit Score: {minTransit}</label>
            <input 
              type="range" min="0" max="800" step="10" value={minTransit} 
              onChange={(e) => setMinTransit(Number(e.target.value))} 
              style={{ width: '100%' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '10px' }}>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px', color: '#555' }}>Min Parks</label>
              <input 
                type="number" min="0" max="30" value={minParks} 
                onChange={(e) => setMinParks(Number(e.target.value))} 
                style={{ width: '100%', padding: '6px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #ccc' }}
              />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px', color: '#555' }}>Min Libraries</label>
              <input 
                type="number" min="0" max="5" value={minLibraries} 
                onChange={(e) => setMinLibraries(Number(e.target.value))} 
                style={{ width: '100%', padding: '6px', boxSizing: 'border-box', borderRadius: '4px', border: '1px solid #ccc' }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '10px', marginTop: '4px' }}>
            <button 
              onClick={fetchRecommendations}
              style={{ flex: 1, backgroundColor: '#27ae60', color: 'white', border: 'none', padding: '10px', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
            >
              {loading ? 'Searching...' : 'Apply Filters'}
            </button>
            <button 
              onClick={exportToCSV}
              title="Download CSV of current results"
              style={{ backgroundColor: '#2980b9', color: 'white', border: 'none', padding: '10px 14px', borderRadius: '4px', fontWeight: 'bold', cursor: 'pointer' }}
            >
              📥 Export
            </button>
          </div>
        </div>

        {/* RESULTS SUMMARY */}
        <div>
          <h4 style={{ margin: '0 0 10px 0', color: '#2c3e50' }}>Matching Neighborhoods ({filteredRecommendations.length})</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {filteredRecommendations.length === 0 ? (
              <p style={{ fontSize: '13px', color: '#7f8c8d', fontStyle: 'italic' }}>No matching areas found.</p>
            ) : (
              filteredRecommendations.map((n) => {
                const isSelected = n.id === selectedId;
                return (
                  <div 
                    key={n.id} 
                    onClick={() => handleSelectNeighborhood(n)}
                    style={{ 
                      background: isSelected ? '#ebf5fb' : 'white', 
                      padding: '12px', 
                      borderRadius: '6px', 
                      boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
                      border: isSelected ? '2px solid #3498db' : '1px solid transparent',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <h5 style={{ margin: '0 0 5px 0', fontSize: '15px', color: '#2c3e50' }}>{n.name}</h5>
                    <div style={{ fontSize: '12px', color: '#555', display: 'flex', justifyContent: 'space-between' }}>
                      <span>Wellness: <strong>{n.wellness_score}</strong></span>
                      <span>Parks: <strong>{n.parks_count}</strong></span>
                      <span>Libraries: <strong>{n.libraries_count}</strong></span>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* INTERACTIVE MAP CONTAINER */}
      <div style={{ flex: 1, height: '100%' }}>
        <MapContainer center={mapCenter} zoom={mapZoom} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <MapController center={mapCenter} zoom={mapZoom} />

          {/* PLOT FILTERED NEIGHBORHOOD MARKERS */}
          {filteredRecommendations.map((n) => {
            if (!n.latitude || !n.longitude) return null;
            const isSelected = n.id === selectedId;
            return (
              <CircleMarker 
                key={n.id}
                center={[n.latitude, n.longitude]}
                radius={isSelected ? 12 : 9}
                fillColor={isSelected ? "#e74c3c" : "#27ae60"}
                color="#ffffff"
                weight={2}
                fillOpacity={0.85}
                eventHandlers={{
                  click: () => setSelectedId(n.id),
                }}
              >
                <Popup>
                  <div style={{ fontSize: '14px', fontFamily: 'sans-serif' }}>
                    <h4 style={{ margin: '0 0 6px 0', color: '#2c3e50' }}>{n.name}</h4>
                    <p style={{ margin: '2px 0' }}>🌿 Wellness Score: <strong>{n.wellness_score}</strong></p>
                    <p style={{ margin: '2px 0' }}>🚇 Transit Score: <strong>{n.transit_score}</strong></p>
                    <p style={{ margin: '2px 0' }}>🌳 Parks: <strong>{n.parks_count}</strong></p>
                    <p style={{ margin: '2px 0' }}>📚 Libraries: <strong>{n.libraries_count}</strong></p>
                  </div>
                </Popup>
              </CircleMarker>
            );
          })}
        </MapContainer>
      </div>

    </div>
  );
}