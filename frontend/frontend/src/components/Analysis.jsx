// components/Analysis.jsx
const getAnalysis = async (lat, lon) => {
  const response = await fetch(`http://127.0.0.1:8000/analyze?lat=${lat}&lon=${lon}&area_name=MyArea`);
  const data = await response.json();
  console.log(data); // Ye JSON tujhe UI pe dikhana hai
}