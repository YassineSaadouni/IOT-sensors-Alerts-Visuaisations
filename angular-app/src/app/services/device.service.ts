import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Device, SearchParams } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getDevices(params?: SearchParams): Observable<ApiResponse<Device>> {
    let httpParams = new HttpParams();
    
    if (params) {
      Object.keys(params).forEach(key => {
        const value = (params as any)[key];
        if (value !== undefined && value !== null && value !== '') {
          httpParams = httpParams.set(key, value.toString());
        }
      });
    }

    return this.http.get<ApiResponse<Device>>(`${this.apiUrl}/devices/`, { params: httpParams });
  }

  getDevice(id: string, index?: string): Observable<Device> {
    let httpParams = new HttpParams();
    if (index) {
      httpParams = httpParams.set('index', index);
    }
    return this.http.get<Device>(`${this.apiUrl}/devices/${id}/`, { params: httpParams });
  }

  search(searchParams: SearchParams): Observable<ApiResponse<Device>> {
    return this.http.post<ApiResponse<Device>>(`${this.apiUrl}/search/`, searchParams);
  }
}
