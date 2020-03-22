export class Editable<T> {
  edit: Boolean;
  item: T;

  constructor(e: Boolean, i: T) {
    this.edit = e;
    this.item = i;
  }
}
