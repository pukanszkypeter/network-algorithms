import {AbstractControl, FormControl, ValidatorFn, Validators} from "@angular/forms";

export interface NetworkType {
  value: string,
  printValue: string
}

export const networkTypes: NetworkType[] = [
  { value: 'complete', printValue: 'Complete'},
  { value: 'simpleLine', printValue: 'Simple Line'},
  { value: 'circle', printValue: 'Circle'},
  { value: 'barbell', printValue: 'Barbell'},
  { value: 'lollipop', printValue: 'Lollipop'},
  { value: 'specialLine', printValue: 'Special Line'},
  { value: 'grid', printValue: 'Grid'},
  { value: 'hypercube', printValue: 'Hypercube'},
  { value: 'er_random', printValue: 'Random'}
];

export function hasNodeValueConstraint(type: string, control: FormControl): void {
  switch (type) {
    case networkTypes[3].value: // Barbell
      control.setValidators([Validators.min(1), Validators.max(1000), Validators.required, barbellConstraint()]);
      control.updateValueAndValidity();
      break;
    case networkTypes[4].value: // Lollipop
      control.setValidators([Validators.min(1), Validators.max(1000), Validators.required, lollipopConstraint()]);
      control.updateValueAndValidity();
      break;
    case networkTypes[7].value: // Hypercube
      control.setValidators([Validators.min(1), Validators.max(1000), Validators.required, hypercubeConstraint()]);
      control.updateValueAndValidity();
      break;
    default:
      control.setValidators([Validators.min(1), Validators.max(1000), Validators.required]);
      control.updateValueAndValidity();
  }
}

export function barbellConstraint(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any} | null =>
    (control.value % 3 != 0) ? {barbellConstraintError: control.value} : null;
}

export function lollipopConstraint(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any} | null =>
    (control.value % 2 != 0) ? {lollipopConstraintError: control.value} : null;
}

export function hypercubeConstraint(): ValidatorFn {
  return (control: AbstractControl): { [key: string]: any} | null => {
    let count = 0;
    let number = control.value;
    while (number) {
      number = number & (number - 1);
      count++;
    }
    return (count != 1) ? {hypercubeConstraintError: control.value}: null;
  }
}