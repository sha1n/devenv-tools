import oscmd


def collect_product_info_files():
    candidates = oscmd.cmd_output_for(["ls", "/Applications"]).split("\n")
    intellij_dirs = filter(lambda d: d.find("IntelliJ") == 0, candidates)

    return map(lambda d: "/Applications/" + d + "/Contents/Resources/product-info.json", intellij_dirs)


def collect_log_libraries(user_home):
    candidates = oscmd.cmd_output_for(["ls", "%s/Library/Logs" % user_home]).split("\n")
    intellij_dirs = filter(lambda d: d.find("Idea") != -1, candidates)

    return map(lambda d: "%s/Library/Logs/%s" % (user_home, d), intellij_dirs)
