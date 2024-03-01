import sys

def main(var_file, con_file, procedure):
    print(var_file)
    print(con_file)
    print(procedure)

if __name__ == "__main__":
    var_file = sys.argv[1]
    con_file = sys.argv[2]
    procedure = sys.argv[3]
    main(var_file, con_file, procedure)