import { exec } from 'child_process';

const startServer = (port) => {
  return new Promise((resolve, reject) => {
    const process = exec(`vite --port ${port}`, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error starting Vite on port ${port}:`, error);
        reject(error);
        return;
      }
      console.log(`Vite started on port ${port}`);
      resolve();
    });

    process.stdout.pipe(process.stdout);
    process.stderr.pipe(process.stderr);
  });
};

const startServers = async (ports) => {
  const startPromises = ports.map((port) => startServer(port));
  await Promise.all(startPromises);
};

const ports = process.argv.slice(2).map(Number);
if (ports.length === 0) {
  console.error('Please provide at least one port number');
  process.exit(1);
}

startServers(ports).then(() => {
  console.log('All servers started');
}).catch((error) => {
  console.error('Error starting servers:', error);
});
