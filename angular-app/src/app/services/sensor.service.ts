import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Sensor, SearchParams, AggregationResult } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class SensorService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getSensors(params?: SearchParams): Observable<ApiResponse<Sensor>> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.keys(params).forEach(key => {
        const value = (params as any)[key];
        if (value !== undefined && value !== null && value !== '') {
          httpParams = httpParams.set(key, value.toString());
        }
      });
    }

    return this.http.get<ApiResponse<Sensor>>(`${this.apiUrl}/sensors/`, { params: httpParams });
  }

  getStatistics(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/sensors/statistics/`);
  }
}
