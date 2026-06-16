import React, { useState } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';

// Map ko nayi location par move karne ke liye helper component
function ChangeMapView({ center }) {
  const map = useMap();
  map.setView(center, map.getZoom());
  return null;
}

export default function App() {
  const [locationName, setLocationName] = useState('Indore');
  const [year, setYear] = useState('2000');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [coords, setCoords] = useState([22.7196, 75.8577]); // Default Indore
  const [searched, setSearched] = useState(false);

  const handleCheck = async () => {
    if (!locationName) {
      alert("Please provide Location");
      return;
    }

    setLoading(true);
    setSearched(true);
    try {
      // 1. Location name se Latitude/Longitude nikalo (Free OpenStreetMap API)
      const geoRes = await axios.get(`https://nominatim.openstreetmap.org/search?format=json&q=${locationName}`);
      
      let lat = coords[0];
      let lon = coords[1];
      
      if (geoRes.data && geoRes.data.length > 0) {
        lat = parseFloat(geoRes.data[0].lat);
        lon = parseFloat(geoRes.data[0].lon);
        setCoords([lat, lon]);
      }

      
// Naya (Render wala):
const response = await axios.get(`https://hackhazard-project.onrender.com/analyze`, {
  params: { lat: lat, lon: lon, past_year: year, area_name: locationName }
});
      
      setData(response.data);
    } catch (error) {
      console.error(error);
      alert("Please Ensure for backend server");
    }
    setLoading(false);
  };

  return (
    // Main Background
    
    <div className="w-full  bg-[rgb(7,8,20)] text-white font-sans flex flex-col  pt-12 px-5">
      
      {/* --- TOP BAR (Search & Controls) --- */}
      <div className="flex items-center justify-center gap-5 mb-12 w-full max-w-3xl mx-auto">

        
        {/* Input & Year Pill */}
        <div className="flex items-center bg-[#2d2d2d] rounded-full px-6 py-3 shadow-lg w-full max-w-2xl">
          <input 
            type="text" 
            placeholder="Enter location" 
            className="bg-transparent outline-none text-white placeholder-gray-400 w-full text-lg"
            value={locationName}
            onChange={(e) => setLocationName(e.target.value)}
          />
          
          {/* Vertical Line Divider */}
          <div className="h-8 w-px bg-gray-600 mx-4"></div>
          
          <input 
            type="text" 
            placeholder="Year" 
            className="bg-transparent outline-none text-white placeholder-gray-400 w-10 text-lg"
            value={year}
            onChange={(e) => setYear(e.target.value)}
          />
        </div>

        {/* Check Button */}
        <button 
          onClick={handleCheck}
          disabled={loading}
          className="bg-[#2d2d2d] hover:bg-[#3d3d3d] text-white px-10 py-3 rounded-full text-lg shadow-lg transition-colors disabled:opacity-50"
        >
          {loading ? 'loading...' : 'check'}
        </button>

      </div>

      {/* --- BOTTOM SECTION (3 Columns) --- */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full px-0 mb-3 h-[640px]">
        
        {/* Box 1: Past Map */}
        <div className="bg-[#161616] rounded-2xl p-4 flex flex-col shadow-xl">
          <h2 className="text-2xl font-semibold mb-4 text-center text-gray-300">Past ({year})</h2>
          <div className="flex-1 rounded-xl overflow-hidden  contrast-125">
            {/* Grayscale filter makes it look like an old map */}
            <MapContainer center={coords} zoom={13} zoomControl={false} style={{ height: '100%', width: '100%' }}>
              <TileLayer
  url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
  attribution="Tiles © Esri & Contributors"
/>
<TileLayer
  url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
  attribution="Labels © Esri"
/>


              <ChangeMapView center={coords} />
            </MapContainer>
          </div>
        </div>

        {/* Box 2: Present Map */}
        <div className="bg-[#161616] rounded-2xl p-4 flex flex-col shadow-xl">
          <h2 className="text-2xl font-semibold mb-4 text-center text-gray-300">Present  (2026)</h2>
          <div className="flex-1 rounded-xl overflow-hidden">
            <MapContainer center={coords} zoom={13} zoomControl={false} style={{ height: '100%', width: '100%' }}>
              <TileLayer
  url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
  attribution="Tiles © Esri & Contributors"
/>
<TileLayer
  url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
  attribution="Labels © Esri"
/>


              <ChangeMapView center={coords} />
            </MapContainer>
          </div>
        </div>

        {/* Box 3: Sarvam AI Response */}
        <div className="bg-[#161616] rounded-2xl p-6 flex flex-col shadow-xl overflow-y-auto">
          <h2 className="text-2xl font-semibold mb-6 text-center text-gray-300">Servam Ai response</h2>
          
          {!searched ? (
            <div className="flex-1 flex items-center justify-center text-gray-500 text-lg text-center">
              Enter location and click check to get analysis.
            </div>
          ) : loading ? (
            <div className="flex-1 flex items-center justify-center text-green-400 text-xl animate-pulse">
              Analyzing Earth Data...
            </div>
          ) : data ? (
            <div className="flex flex-col gap-6">
              <div className="flex justify-between items-center bg-[#1c1c1c] p-4 rounded-xl border border-gray-600">
                <span className="text-gray-400">Past Greenery ({data.past_year})</span>
                <span className="text-2xl font-bold text-red-400">{data.past_greenery}%</span>
              </div>
              <div className="flex justify-between items-center bg-[#1c1c1c] p-4 rounded-xl border border-gray-600">
                <span className="text-gray-400">Present Greenery ({data.present_year})</span>
                <span className="text-2xl font-bold text-green-400">{data.present_greenery}%</span>
              </div>
              
              <div className="bg-[#1c1c1c] p-5 rounded-xl border border-gray-600">
                <h3 className="text-gray-400 mb-2 text-sm uppercase tracking-wider">AI Insight</h3>
                <p className="text-lg leading-relaxed text-gray-100">
                  {data.ai_analysis}
                </p>
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-red-400 text-lg">
              Failed to load data.
            </div>
          )}
        </div>

      </div>
    </div>
  );
}