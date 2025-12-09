import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { DevicesComponent } from './components/devices/devices.component';
import { SensorsComponent } from './components/sensors/sensors.component';
import { FileUploadComponent } from './components/file-upload/file-upload.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { KibanaDashboardComponent } from './kibana-dashboard.component';
import { TestPipelineComponent } from './components/test-pipeline/test-pipeline.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    DevicesComponent,
    SensorsComponent,
    FileUploadComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    KibanaDashboardComponent,  // Import standalone component
    TestPipelineComponent      // Import standalone component
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
