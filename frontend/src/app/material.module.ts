import { NgModule } from '@angular/core';
import {
  MatTableModule, MatButtonModule, MatCheckboxModule, MatInputModule, MatSlideToggleModule, MatToolbarModule, MatSidenavModule,
  MatIconModule, MatGridListModule, MatCardModule, MatDialogModule, MatListModule, MatMenuModule, MatTabsModule,
  MatPaginatorModule, MatRadioModule, MatSnackBarModule, MatExpansionModule, MatSortModule, MatTooltipModule, MatChipsModule,
  MatSliderModule, MatStepperModule, MatSelectModule, MatNativeDateModule, MatProgressSpinnerModule, MatProgressBarModule
} from '@angular/material';

import { MatFormFieldModule } from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CdkTableModule } from '@angular/cdk/table';
import { MatDatepickerModule } from '@angular/material/datepicker';
@NgModule({
  imports: [MatSidenavModule, MatToolbarModule, MatPaginatorModule, MatRadioModule, MatSnackBarModule, MatExpansionModule, MatSortModule,
    BrowserAnimationsModule, MatIconModule, MatGridListModule, MatCardModule, CdkTableModule, MatTableModule, MatButtonModule,
    MatCheckboxModule, MatInputModule, MatSlideToggleModule, MatDialogModule, MatListModule, MatChipsModule, MatMenuModule, MatTabsModule,
    MatTooltipModule, MatChipsModule, MatSliderModule, MatStepperModule, MatFormFieldModule, MatSelectModule, MatDatepickerModule,
    MatNativeDateModule, MatProgressSpinnerModule, MatProgressBarModule],
  exports: [CdkTableModule, MatTableModule, MatPaginatorModule, MatRadioModule, MatSnackBarModule, MatExpansionModule,
    MatSidenavModule, MatToolbarModule, MatButtonModule, MatCheckboxModule, MatInputModule, MatSlideToggleModule,
    MatGridListModule, MatSortModule,
    MatCardModule, BrowserAnimationsModule, MatIconModule, MatDialogModule, MatListModule, MatChipsModule, MatMenuModule, MatTabsModule,
    MatTooltipModule, MatChipsModule, MatSliderModule, MatStepperModule, MatFormFieldModule, MatSelectModule, MatDatepickerModule,
    MatNativeDateModule, MatProgressSpinnerModule, MatProgressBarModule],
  declarations: [],
  //declarations:[MultiselecttabledialogComponent]
})
export class MaterialModule { }
