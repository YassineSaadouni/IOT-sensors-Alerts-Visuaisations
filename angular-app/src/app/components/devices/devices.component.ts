import { Component, OnInit } from '@angular/core';
import { DeviceService } from '../../services/device.service';
import { Device, SearchParams } from '../../models/models';

@Component({
  selector: 'app-devices',
  templateUrl: './devices.component.html',
  styleUrls: ['./devices.component.scss']
})
export class DevicesComponent implements OnInit {
  devices: Device[] = [];
  loading = false;
  error: string | null = null;
  
  // Pagination
  total = 0;
  page = 1;
  pageSize = 20;
  
  // Filtres
  searchQuery = '';
  selectedFileType: 'json' | 'csv' | '' = '';
  selectedStatus = '';
  selectedSource = '';
  sortField = 'timestamp';
  sortDirection: 'asc' | 'desc' = 'desc';
  
  // Options
  fileTypes = ['json', 'csv'];
  statuses = ['active', 'warning', 'critical', 'inactive', 'stopped', 'en_route'];
  sources: string[] = [];

  constructor(private deviceService: DeviceService) {}

  ngOnInit(): void {
    this.loadDevices();
    this.loadSources();
  }

  loadDevices(): void {
    this.loading = true;
    this.error = null;

    const params: SearchParams = {
      size: this.pageSize,
      from: (this.page - 1) * this.pageSize
    };

    if (this.searchQuery) {
      params.query = this.searchQuery;
    }

    if (this.selectedFileType) {
      params.file_type = this.selectedFileType;
    }

    if (this.selectedStatus) {
      params.filters = { status: this.selectedStatus };
    }

    if (this.selectedSource) {
      params.source_file = this.selectedSource;
    }

    if (this.sortField) {
      params.sort = [{
        field: this.sortField,
        order: this.sortDirection
      }];
    }

    this.deviceService.getDevices(params).subscribe({
      next: (response) => {
        this.devices = response.documents;
        this.total = response.total;
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des devices';
        console.error('Error loading devices:', error);
        this.loading = false;
      }
    });
  }

  loadSources(): void {
    // Charger la liste des sources disponibles
    this.deviceService.getDevices({ size: 1000 }).subscribe({
      next: (response) => {
        const sourcesSet = new Set<string>();
        response.documents.forEach(device => {
          if (device.source_file) {
            sourcesSet.add(device.source_file);
          }
        });
        this.sources = Array.from(sourcesSet).sort();
      }
    });
  }

  search(): void {
    this.page = 1;
    this.loadDevices();
  }

  clearFilters(): void {
    this.searchQuery = '';
    this.selectedFileType = '';
    this.selectedStatus = '';
    this.selectedSource = '';
    this.page = 1;
    this.loadDevices();
  }

  changePage(newPage: number): void {
    this.page = newPage;
    this.loadDevices();
  }

  changeSort(field: string): void {
    if (this.sortField === field) {
      this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc';
    } else {
      this.sortField = field;
      this.sortDirection = 'desc';
    }
    this.loadDevices();
  }

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'active': 'badge-success',
      'warning': 'badge-warning',
      'critical': 'badge-danger',
      'inactive': 'badge-secondary',
      'stopped': 'badge-danger',
      'en_route': 'badge-info'
    };
    return statusMap[status] || 'badge-secondary';
  }

  getTotalPages(): number {
    return Math.ceil(this.total / this.pageSize);
  }

  getPageNumbers(): number[] {
    const totalPages = this.getTotalPages();
    const pages: number[] = [];
    const maxPages = 5;
    
    let startPage = Math.max(1, this.page - Math.floor(maxPages / 2));
    let endPage = Math.min(totalPages, startPage + maxPages - 1);
    
    if (endPage - startPage < maxPages - 1) {
      startPage = Math.max(1, endPage - maxPages + 1);
    }
    
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
    
    return pages;
  }

  exportToCSV(): void {
    const csvData = this.convertToCSV(this.devices);
    const blob = new Blob([csvData], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `devices_${new Date().toISOString()}.csv`;
    link.click();
  }

  private convertToCSV(data: Device[]): string {
    const headers = ['ID', 'Type', 'Status', 'Timestamp', 'Source File'];
    const rows = data.map(device => [
      device.device_id || device.capteur_id || device.vehicule_id || '-',
      device.file_type,
      device.status || '-',
      device.timestamp,
      device.source_file || '-'
    ]);

    return [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');
  }
}
