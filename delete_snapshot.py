import subprocess
import re

# 执行命令并获取输出
command = "linstor snapshot list"
result = subprocess.run(command, shell=True, capture_output=True, text=True).stdout

# 正则表达式匹配资源名称和快照名称
pattern = re.compile(r'\|\s*(\w+)\s*\|\s*([\w_]+)\s*\|')

# 解析输出并填充字典
snapshots_dict = {}
for match in pattern.finditer(result):
    resource_name, snapshot_name = match.groups()
    if resource_name not in snapshots_dict:
        snapshots_dict[resource_name] = []
    snapshots_dict[resource_name].append(snapshot_name)

# 打印结果
for resource, snapshots in snapshots_dict.items():
    print(f"{resource}: {snapshots}")

# 遍历字典
for resource, snapshots in snapshots_dict.items():
    for snapshot in snapshots:
        # 构建删除快照的命令
        command = f"linstor snapshot d {resource} {snapshot}"
        # 执行命令
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        # 检查命令执行结果
        if result.returncode == 0:
            print(f"Deleted snapshot {snapshot} of resource {resource} successfully.")
        else:
            print(f"Failed to delete snapshot {snapshot} of resource {resource}. Error: {result.stderr}")