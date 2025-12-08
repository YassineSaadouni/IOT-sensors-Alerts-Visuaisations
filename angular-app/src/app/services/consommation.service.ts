import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ApiResponse, Consommation, ConsommationStats, SearchParams } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ConsommationService {
  private apiUrl = `${environment.apiUrl}/consommation`;

  constructor(private http: HttpClient) {}

  getConsommation(params: SearchParams = {}): Observable<ApiResponse<Consommation>> {
    let httpParams = new HttpParams();
    if (params.q) httpParams = httpParams.set('q', params.q);
    if (params.size) httpParams = httpParams.set('size', params.size.toString());
    if (params.from) httpParams = httpParams.set('from', params.from.toString());
    if (params.sort_by) httpParams = httpParams.set('sort_by', params.sort_by);
    if (params.sort_order) httpParams = httpParams.set('sort_order', params.sort_order);
    
    // Filtres spécifiques
    if (params.filters) {
      Object.keys(params.filters).forEach(key => {
        if (params.filters![key]) {
          httpParams = httpParams.set(key, params.filters![key]);
        }
      });
    }

    return this.http.get<ApiResponse<Consommation>>(this.apiUrl, { params: httpParams });
  }

  getStats(): Observable<ConsommationStats> {
    return this.http.get<ConsommationStats>(`${this.apiUrl}/stats`);
  }
}
