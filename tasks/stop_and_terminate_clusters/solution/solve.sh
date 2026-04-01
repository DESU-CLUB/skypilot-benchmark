#!/bin/bash

cat > /home/user/cleanup.sh << 'EOF'
#!/bin/bash
sky stop --all -y
sky down --all -y
EOF

chmod +x /home/user/cleanup.sh
