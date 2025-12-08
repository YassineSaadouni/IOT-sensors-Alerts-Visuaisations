import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Statistics, HealthStatus, AggregationResult } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getHealth(): Observable<HealthStatus> {
    return this.http.get<HealthStatus>(`${this.apiUrl}/health/`);
  }

  getStatistics(index?: string): Observable<Statistics> {
    const url = index ? `${this.apiUrl}/stats/?index=${index}` : `${this.apiUrl}/stats/`;
    return this.http.get<Statistics>(url);
  }

  aggregate(field: string, aggType: string = 'terms', size: number = 10): Observable<AggregationResult> {
    return this.http.post<AggregationResult>(`${this.apiUrl}/aggregations/`, {
      field,
      agg_type: aggType,
      size
    });
  }
}
