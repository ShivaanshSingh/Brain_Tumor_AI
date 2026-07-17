import { execSync } from 'child_process';
import * as path from 'path';

const action = process.argv[2];
const isWin = process.platform === 'win32';

const rootDir = path.join(__dirname, '..');
const backendDir = path.join(rootDir, 'backend');
const venvPath = path.join(backendDir, 'venv');

const pipPath = isWin 
  ? path.join(venvPath, 'Scripts', 'pip.exe') 
  : path.join(venvPath, 'bin', 'pip');
const pythonPath = isWin 
  ? path.join(venvPath, 'Scripts', 'python.exe') 
  : path.join(venvPath, 'bin', 'python');

// Try to use 'python3' on non-Windows, fallback to 'python' if needed
let pythonCmd = isWin ? 'python' : 'python3';

if (action === 'install') {
  console.log('=== Setting up Python Virtual Environment ===');
  try {
    execSync(`${pythonCmd} -m venv "${venvPath}"`, { stdio: 'inherit' });
  } catch (err) {
    if (!isWin) {
      console.log('python3 not found, trying python...');
      pythonCmd = 'python';
      execSync(`${pythonCmd} -m venv "${venvPath}"`, { stdio: 'inherit' });
    } else {
      throw err;
    }
  }

  console.log('\n=== Installing Backend Dependencies ===');
  const reqPath = path.join(backendDir, 'requirements.txt');
  execSync(`"${pipPath}" install -r "${reqPath}"`, { stdio: 'inherit' });
  console.log('\n=== Backend setup completed successfully! ===');

} else if (action === 'dev') {
  console.log('=== Starting Flask Backend Server ===');
  const appPath = path.join(backendDir, 'app.py');
  execSync(`"${pythonPath}" -u "${appPath}"`, { stdio: 'inherit' });
} else {
  console.error('Unknown action. Use "install" or "dev".');
  process.exit(1);
}
