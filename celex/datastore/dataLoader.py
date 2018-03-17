from sqliteClient import SQLiteClient


class DataLoader(SQLiteClient):

    # columns delimited with '\'    ex: 'wrong\r.Q.N.\r.Q.N.\rQN\r.Q.N.\1'
    # entries delimited with newline character
    # Note on usage: column types assumed to be strings. Must correct within
    #   this function if columns are other types.
    def load_table_from_file(
            self,
            table_to_load,
            file_path,
            column_name_list,
            unique=True):

        first_column_values = set()

        with open(file_path) as file_to_load:
            for line in file_to_load:
                value_dict = {}
                formatted_line = line.strip('\n').split("\\")
                for i, col in enumerate(column_name_list):
                    value_dict[col] = formatted_line[i]
                    if i == 5:
                        value_dict[col] = int(value_dict[col])

                if (value_dict[column_name_list[0]] not in first_column_values
                        or not unique):
                    self.insert_into_table(table_to_load, value_dict)
                    first_column_values.add(value_dict[column_name_list[0]])


if __name__ == "__main__":
    dl = DataLoader("wordforms_db")  # TODO unexpected argument...
    dl.truncate_table("workingresults")
