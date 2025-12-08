import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Vehicle, SearchParams } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class VehicleService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getVehicles(params?: SearchParams): Observable<ApiResponse<Vehicle>> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.keys(params).forEach(key => {
        const value = (params as any)[key];
        if (value !== undefined && value !== null && value !== '') {
          httpParams = httpParams.set(key, value.toString());
        }
      });
    }

    return this.http.get<ApiResponse<Vehicle>>(`${this.apiUrl}/vehicles/`, { params: httpParams });
  }

  getStatistics(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/vehicles/statistics/`);
  }
}
