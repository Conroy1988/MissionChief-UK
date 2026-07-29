const sourcePrefix = '/MissionChief-UK/';
const targetBase = 'https://www.tkb-gaming.scot/games/missionchief/guides/';
const aliases = new Map([
  ['tools/account-readiness/', 'planning/account-readiness/'],
  ['tools/fleet-planner/', 'planning/fleet-planner/'],
  ['tools/mission-lookup/', 'intelligence/missions/'],
  ['tools/planning-tools/', 'planning/'],
  ['tools/query-catalogue/', 'intelligence/missions/'],
  ['tools/resource-comparison/', 'intelligence/resources/'],
]);

export function resolveTarget(pathname = '/', search = '', hash = '') {
  let route = String(pathname).startsWith(sourcePrefix)
    ? String(pathname).slice(sourcePrefix.length)
    : '';
  route = route.replace(/^\/+|\/+$/g, '');
  if (route && !/\.[a-z\d]+$/i.test(route)) route = `${route}/`;

  route = aliases.get(route) ?? route;
  route = route
    .replace(/^assets\/data\/v1\//, 'api/v1/')
    .replace(/^assets\/data\/official\//, 'api/official/');

  return `${targetBase}${route}${String(search)}${String(hash)}`;
}

if (typeof window !== 'undefined') {
  const target = resolveTarget(
    window.location.pathname,
    window.location.search,
    window.location.hash,
  );
  const link = window.document.querySelector('[data-redirect-target]');
  if (link) link.href = target;
  window.location.replace(target);
}
