import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DevicesComponent } from './components/devices/devices.component';
import { SensorsComponent } from './components/sensors/sensors.component';
import { FileUploadComponent } from './components/file-upload/file-upload.component';
import { KibanaDashboardComponent } from './kibana-dashboard.component';
import { TestPipelineComponent } from './components/test-pipeline/test-pipeline.component';

const routes: Routes = [
  { path: '', redirectTo: '/kibana', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'kibana', component: KibanaDashboardComponent },
  { path: 'test-pipeline', component: TestPipelineComponent },
  { path: 'devices', component: DevicesComponent },
  { path: 'sensors', component: SensorsComponent },
  { path: 'upload', component: FileUploadComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
