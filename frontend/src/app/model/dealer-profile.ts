import {Address} from "./address";
import {DealerShortDescription} from "./dealer-short-description";
import {DealerDescription} from "./dealer-description";

export class DealerProfile {
  profileId: string;
  address: Address = new Address();
  owner: string;
  short_description: DealerShortDescription = new DealerShortDescription();
  description: DealerDescription = new DealerDescription();
}
