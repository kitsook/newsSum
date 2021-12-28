import Logger from "./Logger";

export default class Subscriptions {
  static get subscriptions(): Set<string> {
    let subs = new Set<string>();
    try {
      let jsonSubscriptions: { [name: string]: number; } = JSON.parse(localStorage.subs);
      for (let key in jsonSubscriptions) {
        subs.add(key);
      }
    } catch(e) {
      Logger.log("Problem retrieving subscription");
    }
    return subs;
  }

  static updateSubscription(subscriptions: string[]) {
    let jsonSubscriptions: { [name: string]: number; } = {}
    for (let sub of subscriptions) {
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

