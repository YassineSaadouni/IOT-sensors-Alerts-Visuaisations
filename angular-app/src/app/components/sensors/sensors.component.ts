import { Component, OnInit } from '@angular/core';
import { SensorService } from '../../services/sensor.service';
import { Sensor, SensorStatistics } from '../../models/models';

@Component({
  selector: 'app-sensors',
  templateUrl: './sensors.component.html',
  styleUrls: ['./sensors.component.scss']
})
export class SensorsComponent implements OnInit {
  sensors: Sensor[] = [];
  statistics: SensorStatistics | null = null;
  loading = false;
  error: string | null = null;

  // Filters
  selectedLocation = '';
  selectedStatus = '';
  locations: string[] = [];
  statuses = ['active', 'warning', 'critical', 'inactive'];

  // Pagination
  total = 0;
  page = 1;
  pageSize = 20;

  constructor(private sensorService: SensorService) {}

  ngOnInit(): void {
    this.loadSensors();
    this.loadStatistics();
  }

  loadSensors(): void {
    this.loading = true;
    this.error = null;

    const params: any = {
      size: this.pageSize,
      from: (this.page - 1) * this.pageSize
    };

    if (this.selectedLocation) {
      params.filters = { location: this.selectedLocation };
    }

    if (this.selectedStatus) {
      if (params.filters) {
        params.filters.status = this.selectedStatus;
      } else {
        params.filters = { status: this.selectedStatus };
      }
    }

    this.sensorService.getSensors(params).subscribe({
      next: (response) => {
        this.sensors = response.documents;
        this.total = response.total;
        this.loading = false;

        // Extract unique locations
        const locationsSet = new Set<string>();
        response.documents.forEach(sensor => {
          if (sensor.location) {
            locationsSet.add(sensor.location);
          }
        });
        this.locations = Array.from(locationsSet).sort();
      },
      error: (error) => {
        this.error = 'Erreur lors du chargement des capteurs';
        console.error('Error loading sensors:', error);
        this.loading = false;
      }
    });
  }

  loadStatistics(): void {
    this.sensorService.getStatistics().subscribe({
      next: (stats) => {
        this.statistics = stats;
      },
      error: (error) => {
        console.error('Error loading statistics:', error);
      }
    });
  }

  applyFilters(): void {
    this.page = 1;
    this.loadSensors();
  }

  clearFilters(): void {
    this.selectedLocation = '';
    this.selectedStatus = '';
    this.page = 1;
    this.loadSensors();
  }

  refresh(): void {
    this.loadSensors();
    this.loadStatistics();
  }

  changePage(newPage: number): void {
    this.page = newPage;
    this.loadSensors();
  }

  getStatusClass(status: string): string {
    const statusMap: { [key: string]: string } = {
      'active': 'badge-success',
      'warning': 'badge-warning',
      'critical': 'badge-danger',
      'inactive': 'badge-secondary'
    };
    return statusMap[status] || 'badge-secondary';
  }

  getBatteryClass(battery: number): string {
    if (battery >= 80) return 'battery-high';
    if (battery >= 40) return 'battery-medium';
    return 'battery-low';
  }

  getTemperatureClass(temp: number): string {
    if (temp > 30) return 'temp-high';
    if (temp < 15) return 'temp-low';
    return 'temp-normal';
  }

  getHumidityClass(humidity: number): string {
    if (humidity > 70) return 'humidity-high';
    if (humidity < 30) return 'humidity-low';
    return 'humidity-normal';
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
}
