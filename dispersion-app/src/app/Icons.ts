export interface Icon {
    selector: string;
    path: string;
  }
  
  export const icons: Icon[] = [
      {selector: 'play', path: 'assets/icons/play.svg'},
      {selector: 'next', path: 'assets/icons/next.svg'},
      {selector: 'pause', path: 'assets/icons/pause.svg'},
      {selector: 'reset', path: 'assets/icons/reset.svg'},
      {selector: 'settings', path: 'assets/icons/settings.svg'}
  ];