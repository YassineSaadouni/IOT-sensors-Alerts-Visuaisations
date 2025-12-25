import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface SearchRequest {
  query?: string;
  index?: string;
  size?: number;
  from_offset?: number;
  device_id?: string;
  vehicle_id?: string;
  source_file?: string;
  file_type?: string;
  status?: string;
  date_from?: string;
  date_to?: string;
  sort_by?: string;
  sort_order?: string;
}

export interface SearchResult {
  total: number;
  count: number;
  documents: any[];
  from: number;
  size: number;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ElasticsearchSearchService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  /**
   * Search Elasticsearch with filters
   */
  search(request: SearchRequest): Observable<SearchResult> {
    // Remove empty string values to avoid sending them to backend
    const cleanRequest = Object.entries(request).reduce((acc, [key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        acc[key] = value;
      }
      return acc;
    }, {} as any);
    
    console.log('[ElasticsearchSearchService] Sending request:', cleanRequest);
    console.log('[ElasticsearchSearchService] API URL:', `${this.apiUrl}/search/`);
    
    return this.http.post<SearchResult>(`${this.apiUrl}/search/`, cleanRequest);
  }

  /**
   * Quick search across all indices
   */
  quickSearch(query: string, size: number = 20): Observable<SearchResult> {
    return this.search({
      query,
      size,
      sort_by: '@timestamp',
      sort_order: 'desc'
    });
  }

  /**
   * Search specific index
   */
  searchIndex(index: string, query?: string, size: number = 50): Observable<SearchResult> {
    return this.search({
      query,
      index,
      size,
      sort_by: '@timestamp',
      sort_order: 'desc'
    });
  }

  /**
   * Get alertes from Elasticsearch
   */
  getAlertes(params?: any): Observable<SearchResult> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<SearchResult>(`${this.apiUrl}/alertes/`, { params: httpParams });
  }

  /**
   * Get capteurs data from Elasticsearch
   */
  getCapteurs(params?: any): Observable<SearchResult> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<SearchResult>(`${this.apiUrl}/capteurs/`, { params: httpParams });
  }

  /**
   * Get consommation data from Elasticsearch
   */
  getConsommation(params?: any): Observable<SearchResult> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<SearchResult>(`${this.apiUrl}/consommation/`, { params: httpParams });
  }

  /**
   * Get occupation data from Elasticsearch
   */
  getOccupation(params?: any): Observable<SearchResult> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<SearchResult>(`${this.apiUrl}/occupation/`, { params: httpParams });
  }

  /**
   * Get maintenance data from Elasticsearch
   */
  getMaintenance(params?: any): Observable<SearchResult> {
    let httpParams = new HttpParams();
    if (params) {
      Object.keys(params).forEach(key => {
        if (params[key]) {
          httpParams = httpParams.set(key, params[key]);
        }
      });
    }
    return this.http.get<SearchResult>(`${this.apiUrl}/maintenance/`, { params: httpParams });
  }
}
