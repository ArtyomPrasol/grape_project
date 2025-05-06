import axios from "axios";
import API_BASE_URL from '../config/api';

let diagnosesCache = null;

export async function fetchDiagnoses() {
  if (!diagnosesCache) {
    const response = await axios.get(`${API_BASE_URL}/api/diagnoses`);
    console.log("Полученные диагнозы: ", response.data)
    diagnosesCache = response.data;
  }
}

export function getDiagnoses(){
    return diagnosesCache;
}