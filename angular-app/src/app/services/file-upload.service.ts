import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { FileUploadHistory } from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class FileUploadService {
  private uploadUrl = environment.uploadUrl;
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.uploadUrl}/`, formData);
  }

  uploadFileWithType(formData: FormData): Observable<any> {
    return this.http.post(`${this.uploadUrl}/`, formData);
  }

  getRecentUploads(): Observable<{ uploads: FileUploadHistory[] }> {
    return this.http.get<{ uploads: FileUploadHistory[] }>(`${this.apiUrl}/files/recent/`);
  }

  getUploadHistory(): Observable<FileUploadHistory[]> {
    return this.http.get<FileUploadHistory[]>(`${this.apiUrl}/files/recent/`);
  }

  getUploadStats(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/files/stats/`);
  }
}
