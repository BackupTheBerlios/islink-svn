/********************************************************************************/
/* Copyright (c) 2004                                                           */
/* Daniel Sleator, David Temperley, and John Lafferty                           */
/* All rights reserved                                                          */
/*                                                                              */
/* Use of the link grammar parsing system is subject to the terms of the        */
/* license set forth in the LICENSE file included with this software,           */ 
/* and also available at http://www.link.cs.cmu.edu/link/license.html           */
/* This license allows free redistribution and use in source and binary         */
/* forms, with or without modification, subject to certain conditions.          */
/*                                                                              */
/********************************************************************************/

#include "link-includes.h"

void test(char *str, Dictionary dict, Parse_Options opts, int should_work) {
  Sentence sent;
  Linkage       linkage;
  char *        diagram;
  int           num_linkages;

  sent = sentence_create(str, dict);
  if (sent == NULL) {
    fprintf(stderr, "%s\n", lperrmsg);
  } else {
    num_linkages = sentence_parse(sent, opts);
    if (should_work && num_linkages == 0)
      fprintf(stderr, "No linkage found for: '%s'\n", str);
    else if (!should_work && num_linkages > 1)
      fprintf(stderr, "Found spurious linkage for: '%s\n'\n", str);
    if (num_linkages > 0) {
      linkage = linkage_create(0, sent, opts);
      printf("%s\n", diagram = linkage_print_diagram(linkage));
      string_delete(diagram);
      linkage_delete(linkage);
    } /*else
        printf("no linkages found for '%s'\n", str);*/
    sentence_delete(sent);
  }
}

int main() {

  Dictionary    dict;
  Parse_Options opts;

  opts  = parse_options_create();
  dict  = dictionary_create("link_grammar/dict", NULL, NULL, NULL);

  test("hundur bor�ar", dict, opts, TRUE);
  test("hundur er vondur", dict, opts, TRUE);
  test("hundurinn er vondi", dict, opts, FALSE);
  test("hundur er vondi", dict, opts, FALSE);

  test("fj�lskyldur f� b�tur", dict, opts, TRUE);
  test("fj�lskyldur f� ekki b�tur", dict, opts, TRUE);
  test("fj�lskyldur f� b�tur � Bretlandi", dict, opts, TRUE);
  test("fj�lskyldur f� ekki b�tur � Bretlandi", dict, opts, TRUE);
  test("fj�lskyldur hry�juverkamanna f� ekki b�tur � Bretlandi", dict, opts, TRUE);
  test("fj�lskyldur gruna�ra hry�juverkamanna f� ekki b�tur � Bretlandi", dict, opts, TRUE);

  test("hundurinn bor�ar vel", dict, opts, TRUE);
  test("hundurinn bor�ar vel heima", dict, opts, TRUE);
  test("hundurinn bor�ar ekki vel heima", dict, opts, TRUE);
  test("hundurinn bor�ar vel ekki heima", dict, opts, FALSE);
  test("hundurinn bor�ar vel heima ekki", dict, opts, FALSE);
  test("hundurinn bor�ar matinn vel heima", dict, opts, TRUE);
  test("hundurinn bor�ar vel matinn heima", dict, opts, FALSE);
  test("hundurinn bor�ar ekki vel matinn heima", dict, opts, FALSE);
  test("hundurinn bor�ar matinn ekki", dict, opts, TRUE);
  test("hundurinn bor�ar ekki matinn", dict, opts, TRUE);
  test("hundurinn bor�ar ekki matinn vel heima", dict, opts, TRUE);
  test("hundurinn bor�ar matinn ekki vel heima", dict, opts, TRUE);
  test("hundurinn bor�ar matinn vel ekki heima", dict, opts, FALSE);
  test("hundurinn bor�ar matinn vel flj�tt", dict, opts, FALSE);
  test("hundurinn bor�ar matinn hratt � Bretlandi", dict, opts, TRUE);
  test("hundurinn bor�ar matinn miklu hra�ar � Bretlandi", dict, opts, TRUE);
  test("hundurinn bor�ar matinn ekki miklu hra�ar � Bretlandi", dict, opts, TRUE);
  test("hundurinn bor�ar matinn ekki oft miklu hra�ar � Bretlandi", dict, opts, TRUE);
  test("hundurinn bor�ar matinn ekki oft ekki miklu hra�ar � Bretlandi", dict, opts, TRUE);


  test("hundurinn bor�ar vel", dict, opts, TRUE);
  test("hundurinn bor�ar betur", dict, opts, TRUE);
  test("hundurinn bor�ar best", dict, opts, TRUE);

  test("hundurinn f�r heim", dict, opts, TRUE);
  test("hundurinn f�r beint heim", dict, opts, TRUE);
  test("hundurinn f�r beint heim � g�r", dict, opts, TRUE);

  dictionary_delete(dict);
  parse_options_delete(opts);

  return 0;
}
