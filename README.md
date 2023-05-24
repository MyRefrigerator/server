# My Refrigerator

## Get Started

| 상황 | 명령어 |
| ---- | ------ |
| 환경 불러오기 | `conda env create -f conda.yaml` |
| 환경 내보내기 | `conda env export > conda.yaml` |
| 환경 실행하기 | `conda activate my-refrigerator` |

<details>
<summary>
참고자료
</summary>

- [[Anaconda] 아나콘다 가상환경 Export 및 Import 하는 방법](https://mentha2.tistory.com/46)
- [[Anaconda] 아나콘다 환경 export, import, clone 하기](https://jh-bk.tistory.com/35)
</details>

<br>

### History

```cmd
conda create -n my-refrigerator -y

conda activate my-refrigerator

[after]
pip install opencv-python
pip install matplotlib
conda install -c conda-forge tesseract
conda install tesseract-ocr
conda install libtesseract-dev
pip install pytesseract
```