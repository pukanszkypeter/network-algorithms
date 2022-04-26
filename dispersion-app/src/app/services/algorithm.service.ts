import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AlgorithmService {

  constructor(private http: HttpClient) { }

  stepDFS(graph: any, start: number, robotSize: number): Observable<any> {
    return this.http.post<any>(
      'http://localhost:4200/api/dfs', {graph: graph, start: start, robotGroup: null, robotSize: robotSize}
    );
  }

}
