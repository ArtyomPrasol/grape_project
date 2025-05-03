import axios from "axios";

let diagnosesCache = null;

export async function fetchDiagnoses() {
  if (!diagnosesCache) {
    const response = await axios.get('http://127.0.0.1:5000/api/diagnoses');
    console.log("Полученные диагнозы: ", response.data)
    diagnosesCache = response.data;
  }
}

export function getDiagnoses(){
    return diagnosesCache;
}