import openpyxl

class Category():
    
    def __init__(
        self,
        topGroup: str,
        midGroup: str,
        group: str
    ):
        self.topGroup = topGroup;
        self.midGroup = midGroup;
        self.group = group;
        
    def get_property(self):
        return {
            'topGroup': self.topGroup,
            'midGroup': self.midGroup,
            'group': self.group
        }

def get_category_list(
    file_path: str = "식품분류기준.xlsx"
) -> list:
    
    # 엑셀 파일 열기
    workbook = openpyxl.load_workbook(file_path)

    # 시트 선택
    sheet = workbook.active

    # 행 단위로 데이터 처리
    categoryList = []
    prevTopGroup = None
    prevMidGroup = None

    row_idx = 0
    for row in sheet.iter_rows(values_only=True):

        row_idx = row_idx + 1
        
        if row_idx == 1:
            continue
        
        nowTopGroup = None
        nowMidGroup = None
        nowGroup = None
        
        for idx, cell in enumerate(row):
            
            if idx == 0:
                
                if cell == None:
                    nowTopGroup = prevTopGroup
                    
                else:
                    nowTopGroup = cell
                    prevTopGroup = cell
                    prevMidGroup = None
            
            elif idx == 1:
                
                if cell == None:
                    nowMidGroup = prevMidGroup
                else:
                    nowMidGroup = cell
                    prevMidGroup = cell
            
            elif idx == 2:
                
                if cell == None:
                    continue
                else:
                    nowGroup = cell
        
        category = Category(nowTopGroup, nowMidGroup, nowGroup)
        categoryList.append(category)
    return categoryList

def save_category_list_as_json(
    category_list: list,
    save_path: str = '식품분류기준.json',
):
    
    import json
    
    with open(save_path, "w", encoding="utf-8") as json_file:
        json.dump(category_list, json_file, ensure_ascii=False)

def save_category_list_as_yaml(
    category_list: list,
    save_path: str = '식품분류기준.yaml',
):
    
    import yaml

    with open(save_path, "w", encoding="utf-8") as yaml_file:
        yaml.dump(category_list, yaml_file, allow_unicode=True, encoding='utf-8')

if __name__ == "__main__":
    
    category_list = get_category_list()
    category_list = [ category.get_property() for category in category_list ]
    
    save_category_list_as_json(category_list)
    save_category_list_as_yaml(category_list)