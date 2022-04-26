import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { SimulationState } from '../models/SimulationState';

@Injectable({
  providedIn: 'root'
})
export class AlgorithmService {

  constructor(private http: HttpClient) { }

  stepDFS(simulationState: SimulationState): Observable<any> {
    return this.http.post<any>(
      'http://localhost:4200/api/dfs', simulationState
    );
  }

}
