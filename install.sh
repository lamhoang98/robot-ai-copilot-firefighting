#!/bin/bash
echo ""
echo "========================================"
echo "Robot AI Copilot - Installation"
echo "========================================"
echo ""
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not installed"
    exit 1
fi
echo "[1/5] Python OK"
python3 --version
echo "[2/5] Creating venv..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
echo "[3/5] Activating..."
source venv/bin/activate
echo "[4/5] Installing packages..."
pip install -q --upgrade pip
pip install -r requirements.txt
echo "[5/5] Creating directories..."
mkdir -p output/logs models
cat > Run_Robot_AI.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py
EOF
chmod +x Run_Robot_AI.sh
echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Next: ./Run_Robot_AI.sh"
echo ""
