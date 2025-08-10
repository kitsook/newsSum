import Logger from "./Logger";

export default class Subscriptions {
  static get subscriptions(): Set<string> {
    const subs = new Set<string>();
    try {
      const jsonSubscriptions: { [name: string]: number; } = JSON.parse(localStorage.subs);
      for (const key in jsonSubscriptions) {
        subs.add(key);
      }
    } catch(e) {
      Logger.log("Problem retrieving subscription: " + e);
    }
    return subs;
  }

  static updateSubscription(subscriptions: string[]) {
    const jsonSubscriptions: { [name: string]: number; } = {}
    for (const sub of subscriptions) {
      jsonSubscriptions[sub] = 1
    }
    localStorage.subs = JSON.stringify(jsonSubscriptions);
  }

  static getLastRead(): string {
    return localStorage.last;
  }

  static setLastRead(sub: string) {
    localStorage.last = sub;
  }
}

