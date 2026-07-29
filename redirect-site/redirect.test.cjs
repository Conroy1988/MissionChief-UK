const assert = require('node:assert/strict');

(async () => {
  const { resolveTarget } = await import('./redirect.js');
  const target = 'https://www.tkb-gaming.scot/games/missionchief/guides/';

  assert.equal(resolveTarget('/MissionChief-UK/'), target);
  assert.equal(
    resolveTarget('/MissionChief-UK/services/fire-and-rescue/'),
    `${target}services/fire-and-rescue/`,
  );
  assert.equal(
    resolveTarget('/MissionChief-UK/tools/account-readiness/', '?scenario=1', '#reserve'),
    `${target}planning/account-readiness/?scenario=1#reserve`,
  );
  assert.equal(
    resolveTarget('/MissionChief-UK/assets/data/v1/missions.json'),
    `${target}api/v1/missions.json`,
  );
  assert.equal(
    resolveTarget('/MissionChief-UK/assets/data/official/uk-missions.json'),
    `${target}api/official/uk-missions.json`,
  );

  console.log('MissionChief GitHub Pages redirect mapping passed.');
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
