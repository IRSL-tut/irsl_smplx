# irsl_smplx

# smplx

https://github.com/vchoutas/smplx

# Usage

## Downloading the model(smplx)

## Install

```bash
sudo apt install venv
python3 -m venv venv
source venv/bin/activate
pip install 'smplx[all]'
```

```python
import smplx_util as su
models = su.genModels()
j = su.genInitialJoints(su.m_male_flat)
di = DrawInterface()
p = su.genDefaultParameters()
out = su.getOutput(su.m_male_flat, params=p)
su.drawBodyShape(su.m_male_flat, out, di)

a.rotate(PI/2, coordinates.X)
a.rotate(PI/2, coordinates.Z, wrt=coordinates.wrt.world)
```
