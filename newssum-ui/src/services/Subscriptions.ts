import Logger from "./Logger";

export default class Subscriptions {
  static jsonSubscriptions: { [name: string]: number; } = JSON.parse(localStorage.subs);

  static get subscriptions(): Set<string> {
    let subs = new Set<string>();
    for (let key in this.jsonSubscriptions) {
      subs.add(key);
    }
    return subs;
  }

  static addSubscription(newSub: string): void {
      this.jsonSubscriptions[newSub] = 1;
      localStorage.subs = JSON.stringify(this.jsonSubscriptions);
  }
}

