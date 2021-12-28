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

  static updateSubscription(subscriptions: string[]) {
    this.jsonSubscriptions = {}
    for (let sub of subscriptions) {
      this.jsonSubscriptions[sub] = 1
    }
    localStorage.subs = JSON.stringify(this.jsonSubscriptions);
  }

  static getLastRead(): string {
    return localStorage.last;
  }

  static setLastRead(sub: string) {
    localStorage.last = sub;
  }
}

